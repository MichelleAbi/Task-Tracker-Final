# --- POST /tasks ---

def test_create_task_valid_returns_201_with_full_body(client):
    r = client.post("/tasks", json={"title": "Test task"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Test task"
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_create_task_missing_title_returns_422(client):
    r = client.post("/tasks", json={})
    assert r.status_code == 422


def test_create_task_blank_title_returns_422(client):
    r = client.post("/tasks", json={"title": "   "})
    assert r.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    r = client.post("/tasks", json={"title": "Test task", "priority": "bogus"})
    assert r.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    r = client.post("/tasks", json={"title": "Test task", "unknown_field": "value"})
    assert r.status_code == 422


# --- GET /tasks ---

def test_list_tasks_empty_returns_200_and_empty_list(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client, created_task):
    r = client.get("/tasks", params={"status": "Done"})
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "Low one", "priority": "Low"})
    client.post("/tasks", json={"title": "High one", "priority": "High"})

    r = client.get("/tasks", params={"priority": "High"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["priority"] == "High"


# --- GET /tasks/{id} ---

def test_get_task_by_id_returns_task(client, created_task):
    r = client.get(f"/tasks/{created_task['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created_task["id"]


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    r = client.get("/tasks/nonexistent-id")
    assert r.status_code == 404
    assert "detail" in r.json()


# --- PATCH /tasks/{id} ---

def test_patch_partial_update_keeps_other_fields(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"title": "Renamed"})
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == "Renamed"
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]


def test_patch_not_found_returns_404(client):
    r = client.patch("/tasks/nonexistent-id", json={"title": "Renamed"})
    assert r.status_code == 404


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "InProgress"})
    assert r.status_code == 200
    assert r.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "Done"})
    assert r.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "ToDo"})
    assert r.status_code == 422


# --- DELETE /tasks/{id} ---

def test_delete_existing_returns_204_no_body(client, created_task):
    r = client.delete(f"/tasks/{created_task['id']}")
    assert r.status_code == 204
    assert r.content == b""


def test_delete_missing_returns_404(client):
    r = client.delete("/tasks/nonexistent-id")
    assert r.status_code == 404

# --- PATCH /tasks/{id} - additional edge cases (E1-E2) ---

def test_patch_valid_transition_inprogress_to_done_returns_200(client, created_task):
    client.patch(f"/tasks/{created_task['id']}", json={"status": "InProgress"})
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "Done"})
    assert r.status_code == 200
    assert r.json()["status"] == "Done"


def test_patch_valid_transition_done_to_inprogress_returns_200(client, created_task):
    client.patch(f"/tasks/{created_task['id']}", json={"status": "InProgress"})
    client.patch(f"/tasks/{created_task['id']}", json={"status": "Done"})
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "InProgress"})
    assert r.status_code == 200
    assert r.json()["status"] == "InProgress"


def test_patch_empty_body_returns_200_no_op(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={})
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == created_task["title"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]


def test_patch_blank_title_returns_422(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"title": "   "})
    assert r.status_code == 422


def test_patch_invalid_status_value_returns_422(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "Blocked"})
    assert r.status_code == 422


def test_patch_invalid_priority_value_returns_422(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"priority": "Urgent"})
    assert r.status_code == 422    

# --- Due dates + overdue filter ---

def test_create_task_with_valid_due_date_returns_201(client):
    r = client.post("/tasks", json={"title": "Task with due date", "due_date": "2099-01-01"})
    assert r.status_code == 201
    assert r.json()["due_date"] == "2099-01-01"


def test_create_task_with_invalid_due_date_format_returns_422(client):
    r = client.post("/tasks", json={"title": "Bad date", "due_date": "not-a-date"})
    assert r.status_code == 422


def test_task_with_past_due_date_is_overdue(client):
    r = client.post("/tasks", json={"title": "Overdue task", "due_date": "2020-01-01"})
    assert r.status_code == 201
    assert r.json()["is_overdue"] is True


def test_done_task_with_past_due_date_is_not_overdue(client):
    r = client.post("/tasks", json={"title": "Done overdue", "due_date": "2020-01-01", "status": "InProgress"})
    task_id = r.json()["id"]
    client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    r2 = client.get(f"/tasks/{task_id}")
    assert r2.json()["is_overdue"] is False


def test_patch_update_due_date(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"due_date": "2099-06-15"})
    assert r.status_code == 200
    assert r.json()["due_date"] == "2099-06-15"


def test_patch_clear_due_date(client):
    created = client.post("/tasks", json={"title": "Has due date", "due_date": "2099-01-01"}).json()
    r = client.patch(f"/tasks/{created['id']}", json={"due_date": None})
    assert r.status_code == 200
    assert r.json()["due_date"] is None


def test_filter_overdue_returns_only_overdue_tasks(client):
    client.post("/tasks", json={"title": "Not overdue", "due_date": "2099-01-01"})
    client.post("/tasks", json={"title": "Overdue", "due_date": "2020-01-01"})
    r = client.get("/tasks", params={"overdue": "true"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["title"] == "Overdue"


# --- Tags ---

def test_create_task_with_tags_returns_201(client):
    r = client.post("/tasks", json={"title": "Tagged task", "tags": ["urgent", "backend"]})
    assert r.status_code == 201
    assert r.json()["tags"] == ["urgent", "backend"]


def test_create_task_with_blank_tag_returns_422(client):
    r = client.post("/tasks", json={"title": "Bad tag", "tags": ["urgent", "  "]})
    assert r.status_code == 422


def test_create_task_deduplicates_tags(client):
    r = client.post("/tasks", json={"title": "Dup tags", "tags": ["urgent", "urgent"]})
    assert r.status_code == 201
    assert r.json()["tags"] == ["urgent"]


def test_patch_update_tags(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"tags": ["new-tag"]})
    assert r.status_code == 200
    assert r.json()["tags"] == ["new-tag"]


def test_patch_without_tags_preserves_existing_tags(client):
    created = client.post("/tasks", json={"title": "Keep tags", "tags": ["keep-me"]}).json()
    r = client.patch(f"/tasks/{created['id']}", json={"title": "Renamed"})
    assert r.status_code == 200
    assert r.json()["tags"] == ["keep-me"]


def test_filter_by_tag_returns_only_matching_tasks(client):
    client.post("/tasks", json={"title": "Has tag", "tags": ["design"]})
    client.post("/tasks", json={"title": "No tag"})
    r = client.get("/tasks", params={"tag": "design"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["title"] == "Has tag"    