def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.json.get("status") == "ok"

def test_register_login_logout(client):
    r = client.post("/register", data={"email":"me@test.com","password":"secret123"}, follow_redirects=True)
    assert r.status_code == 200
    r = client.post("/login", data={"email":"me@test.com","password":"secret123"}, follow_redirects=True)
    assert r.status_code == 200
    r = client.post("/logout", follow_redirects=True)
    assert r.status_code == 200
