def test_index_page(client):
    """Test index page accessibility"""
    response = client.get('/')
    data = response.data.decode('UTF-8')

    assert response.status_code == 200
    assert 'index' in data
