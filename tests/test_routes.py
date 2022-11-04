def test_get_all_planet_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Ocean Planet",
        "description": "watr 4evr",
        "moons": 2
    }
def test_get_one_plant_with_no_data_returns_404(client):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404

def test_create_one_planet(client):
    # Act
    response = client.post("/planets", json={
        "name": "New Book",
        "description": "The Best!",
        "moons": 424
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 201
    assert response_body == "Planet New Book successfully created"

def test_delete_one_planet(client, two_saved_planets):
    response = client.delete('/planets/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"message": "Planet 1 successfully deleted."}
    