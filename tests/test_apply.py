def test_apply(flask_test_client):
    # When
    test_user = "test_user"
    url = f'/model?user={test_user}'
    subject = flask_test_client.post(url)
    # Then
    assert subject.status_code == 200
    assert subject.json == "Model applied"