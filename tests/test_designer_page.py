import allure


from pages.designer_page import DesignerPageLocators


class TestDesignerPage:
    @allure.title("Проверка открытия модального окна ингредиента")
    def test_open_ingredient_modal_window(self, driver, designer_page):
        designer_page.open_design_page()
        designer_page.open_ingredient_details()
        assert designer_page.get_ingredient_window_title() == "Детали ингредиента"

    @allure.title("Проверка закрытия модального окна ингредиента")
    def test_close_ingredient_modal_window(self, driver, designer_page):
        designer_page.open_design_page()
        designer_page.open_ingredient_details()
        designer_page.close_ingredient_details()
        assert designer_page.check_visibility_of_modal_title()

    @allure.title("Счетчик ингредиента увеличивается, когда ингредиент добавлен в корзину")
    def test_ingredient_counter_increase_when_add_to_basket(self, driver, designer_page):
        designer_page.open_design_page()
        counter_before = designer_page.get_ingredient_count()
        designer_page.drag_ingredient_to_basket(DesignerPageLocators.INGREDIENT_LOCATOR)
        counter_after = designer_page.get_ingredient_count()
        assert int(counter_before) + 1 == int(counter_after)

    @allure.title("Авторизированный пользователь может сделать заказ")
    def test_authorized_user_should_make_order(self, driver, user, login_page, designer_page):
        login_page.open_login_page()
        login_page.authorize_user(login=user.login, password=user.password)
        designer_page.make_order_with_bun_and_ingredient()
        assert designer_page.check_order_confirmation()
