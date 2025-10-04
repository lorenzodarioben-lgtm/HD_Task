def test_list_and_item_crud(client):
    client.post("/register", data={"email":"u@test.com","password":"secret123"}, follow_redirects=True)
    client.post("/login", data={"email":"u@test.com","password":"secret123"}, follow_redirects=True)

    r = client.post("/lists/new", data={"name":"Groceries"}, follow_redirects=True)
    assert r.status_code == 200

    r = client.get("/")
    import re
    m = re.search(rb"/lists/(\d+)", r.data); assert m
    list_id = m.group(1).decode()

    r = client.post(f"/lists/{list_id}/items", data={"name":"Milk","quantity":"2","priority":"high"}, follow_redirects=True)
    assert r.status_code == 200 and b"Milk" in r.data

    m = re.search(rb"/items/(\d+)/toggle", r.data); assert m
    item_id = m.group(1).decode()

    assert client.post(f"/items/{item_id}/toggle", follow_redirects=True).status_code == 200
    assert client.post(f"/items/{item_id}/delete", follow_redirects=True).status_code == 200
    assert client.post(f"/lists/{list_id}/delete", follow_redirects=True).status_code == 200
