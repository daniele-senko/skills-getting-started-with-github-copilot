def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    # Arrange

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_adds_participant(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.post("/activities/Soccer%20Team/signup", params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()["Soccer Team"]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up new.student@mergington.edu for Soccer Team"}
    assert email in participants


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess%20Club/signup", params={"email": email})
    participants = client.get("/activities").json()["Chess Club"]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered michael@mergington.edu from Chess Club"}
    assert email not in participants


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    email = "missing@mergington.edu"

    # Act
    response = client.delete("/activities/Soccer%20Team/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
