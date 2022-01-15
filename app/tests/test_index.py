def test_index_page(client):
    """Test index page accessibility"""
    response = client.get('/')
    assert response.status_code == 200
