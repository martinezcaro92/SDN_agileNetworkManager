def test_delete_all_topologies(test_app):
    response = test_app.delete("/topologies/")
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'message': 'Successfully deleted'}

def test_delete_all_controllers(test_app):
    response = test_app.delete("/controllers/")
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'message': 'Successfully deleted'}

def test_delete_flow(test_app):
    response = test_app.delete("/flows/")
    assert response.status_code == 200
    assert response.json() == {"code": 200, "message": "Successfully deleted"}

def test_delete_all_controllers(test_app):
    # controller_id, response_2 = test_post_controllers(test_app=test_app)
    response = test_app.delete("/controllers/")
    print(response)
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'message': 'Successfully deleted'}