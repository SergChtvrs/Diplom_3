import allure
import pytest

from helpers import make_order


class TestOrderFeedPage:
    @allure.title('По клику на заказ, открывается всплывающее окно с деталями')
    def test_open_order_details(self, driver, order_feed_page):
        order_feed_page.open_order_feed_page()
        order_number_from_feed = order_feed_page.get_order_number_from_feed()
        order_feed_page.open_order_details()
        order_number_from_details = order_feed_page.get_order_number_from_order_details()
        assert order_number_from_feed == order_number_from_details

    @allure.title('Заказы пользователя из раздела "История заказов" отображаются на странице "Лента заказов"')
    def test_user_order_displayed_in_order_feed(self, driver, user, login_page,
                                                order_feed_page, header_page, account_page):
        make_order(user.access_token)
        login_page.open_login_page()
        login_page.authorize_user(login=user.login, password=user.password)
        header_page.click_to_account_button()
        account_page.click_to_order_history_button()
        order_number_from_account = account_page.get_order_number()
        header_page.click_to_order_feed_button()
        order_feed_page.scroll_to_order(order_number_from_account)
        order_number_from_order_feed = order_feed_page.get_specific_order_from_order_feed(order_number_from_account)
        assert order_number_from_order_feed == order_number_from_account

    @pytest.mark.parametrize('counter',
                             [
                                 'Выполнено за все время:',
                                 'Выполнено за сегодня:'
                             ],
                             ids=['выполнено за все время',
                                  'выполнено за сегодня']
                             )
    @allure.title('Заказы пользователя из раздела "История заказов" отображаются на странице "Лента заказов"')
    def test_completed_orders_increase_when_user_make_order(self, driver, user, counter, order_feed_page):
        order_feed_page.open_order_feed_page()
        orders_count_before = order_feed_page.get_completed_orders_count(counter)
        make_order(user.access_token)
        orders_count_after = order_feed_page.get_completed_orders_count(counter)
        assert orders_count_before < orders_count_after

    @allure.title('Заказы пользователя из раздела "История заказов" отображаются на странице "Лента заказов"')
    def test_order_displayed_in_in_progress_feed_when_user_make_order(self, driver, user, order_feed_page):
        order_feed_page.open_order_feed_page()
        order = make_order(user.access_token)
        assert order_feed_page.get_order_in_progress(order) == order
