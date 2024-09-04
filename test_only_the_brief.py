import logging
import warnings
logging.captureWarnings(True)
warnings.filterwarnings('default', category=DeprecationWarning, module='myapp')
logger = logging.getLogger('py.warnings')
handler = logging.FileHandler('warnings.log')
logger.addHandler(handler)
from playwright.sync_api import Page, expect
from playwright_recaptcha import recaptchav2

url = 'https://only.digital/projects#brief'


def test_full_fill(page: Page):
    page.goto(url)
    page.get_by_placeholder("Имя*").fill("test")
    page.get_by_placeholder("E-mail*").fill("test@test.com")
    page.get_by_placeholder("Телефон").fill("9999999999")
    page.get_by_placeholder("Компания").fill("test_company")
    page.get_by_text('5–10 млн').check()
    page.get_by_text('Давно знаю').check()
    locator = page.frame_locator("iframe[title='reCAPTCHA']").locator('div.recaptcha-checkbox-border')
    locator.click()
    page.wait_for_timeout(5000)
    with recaptchav2.SyncSolver(page) as solver:
        solver.solve_recaptcha()
    page.get_by_text('Отправить').click()
    expect(page.get_by_text('Заявка успешно отправлена ')).to_be_visible()


def test_attach_file(page: Page):
    page.goto(url)
    with open('test.pdf'):
        page.get_by_label('Прикрепить файл').set_input_files('test.pdf')
    expect(page.get_by_text('test.pdf')).to_be_attached()


def test_checkbox(page: Page):
    page.goto(url)
    page.get_by_text('Комплекс работ').check()
    page.get_by_text('UX-аудит').check()
    expect(page.get_by_text('Комплекс работ')).to_be_checked()
    expect(page.get_by_text('UX-аудит')).to_be_checked()


def test_radiobutton_budget(page: Page):
    page.goto(url)
    page.get_by_text('5–10 млн').check()
    page.get_by_text('3–5 млн').check()
    expect(page.get_by_text('3–5 млн')).to_be_checked()
    expect(page.get_by_text('5–10 млн')).not_to_be_checked()


def test_radiobutton_info(page: Page):
    page.goto(url)
    page.get_by_text('Давно знаю').check()
    expect(page.get_by_text('Давно знаю')).to_be_checked()


def test_change_focus_from_name(page: Page):
    page.goto(url)
    page.get_by_placeholder("Имя*").click()
    page.get_by_text('Ваши контакты').click()
    expect(page.get_by_text('Обязательное поле')).to_be_visible()


def test_change_focus_from_email(page: Page):
    page.goto(url)
    page.get_by_placeholder("E-mail*").click()
    page.get_by_text('Ваши контакты').click()
    expect(page.get_by_text('Обязательное поле')).to_be_visible()


def test_change_focus_from_phone(page: Page):
    page.goto(url)
    page.get_by_placeholder("Телефон").click()
    page.get_by_text('Ваши контакты').click()
    expect(page.get_by_text('Обязательное поле')).to_be_visible()


def test_change_focus_from_company(page: Page):
    page.goto(url)
    page.get_by_placeholder("Компания").click()
    page.get_by_text('Ваши контакты').click()
    expect(page.get_by_text('Обязательное поле')).to_be_visible()