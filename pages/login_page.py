class LoginPage:

    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        self.page.fill("input[name='username']", username)
        self.page.fill("input[name='password']", password)
        self.page.click("button[type='submit']")

    def logout(self):
        self.page.get_by_role("banner").get_by_role("img", name="profile picture").click()
        self.page.get_by_role("menuitem", name="Logout").click()

