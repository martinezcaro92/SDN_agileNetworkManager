def test_delete_all_topologies(test_app):
    response = test_app.delete("/topologies/")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Successfully deleted'}

def test_delete_all_controllers(test_app):
    response = test_app.delete("/controllers/")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Successfully deleted'}
