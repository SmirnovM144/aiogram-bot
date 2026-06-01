"""
Callback query handlers for button interactions.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from aiogram_calendar import SimpleCalendarCallback, SimpleCalendar

from core.constants import (
    CAKE_NAMES, SIZES, LOGISTICS, MAX_ORDERS_PER_DATE, OWNER_PHOTO_ID
)
from database import Database
from forms.user import Form
from handlers.keyboards.main import Keyboards
from utils.validators import Validators


router = Router()

# Global database instance (will be set in main.py)
db: Database = None
# Keyboard and validator instances
kb = Keyboards()
validator = Validators()


def setup_database(database: Database) -> None:
    """Set global database instance."""
    global db
    db = database


# ======================= NAVIGATION CALLBACKS =======================

@router.callback_query(lambda c: c.data == "back")
async def back(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle back button press."""
    await callback.answer("Вы вернулись в главное меню.")
    await state.clear()
    await callback.message.answer("Главное меню:", reply_markup=kb.get_main_menu())


@router.callback_query(lambda c: c.data == "skip")
async def skip(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle skip button press."""
    await callback.answer("Вы пропустили этот шаг.")
    await state.update_data(media_type=None, media=None)
    await state.set_state(Form.additional_info)
    await callback.message.answer(
        "Если у Вас есть дополнительная информация или пожелания, пожалуйста, напишите."
    )


# ======================= CATALOG CALLBACKS =======================

@router.callback_query(lambda c: c.data == "catalog")
async def catalog(callback: CallbackQuery) -> None:
    """Display catalog items."""
    await callback.answer()

    items = await db.get_catalog()

    if not items:
        await callback.message.answer(
            "Каталог пока пуст 😢",
            reply_markup=kb.get_back_keyboard()
        )
        return

    await callback.message.answer("🛍 Каталог:")

    for item in items:
        text = f"{item['title']}\n\n{item['description']}"

        if item.get("file_id"):
            await callback.message.answer_photo(
                photo=item["file_id"],
                caption=text,
                parse_mode="HTML",
                reply_markup=kb.get_back_keyboard()
            )
        else:
            await callback.message.answer(
                text,
                parse_mode="HTML",
                reply_markup=kb.get_back_keyboard()
            )


# ======================= WORKS CALLBACKS =======================

@router.callback_query(lambda c: c.data == "view_works")
async def view_works(callback: CallbackQuery) -> None:
    """Display user's works."""
    await callback.answer("Вы выбрали посмотреть мои работы.")

    works = await db.get_works()

    if not works:
        await callback.message.answer(
            "Пока нет работ 😢",
            reply_markup=kb.get_back_keyboard()
        )
        return

    media = []

    for index, work in enumerate(works):
        caption = "📸 Мои работы" if index == 0 else None

        if work["media_type"] == "photo":
            media.append(
                InputMediaPhoto(
                    media=work["file_id"],
                    caption=caption
                )
            )
        elif work["media_type"] == "video":
            media.append(
                InputMediaVideo(
                    media=work["file_id"],
                    caption=caption
                )
            )

    # Send media in batches (Telegram limit is 10 per group)
    for i in range(0, len(media), 10):
        await callback.message.answer_media_group(media=media[i:i + 10])

    await callback.message.answer(
        "Здесь вы можете посмотреть мои работы.",
        reply_markup=kb.get_back_keyboard()
    )


# ======================= REVIEWS CALLBACKS =======================

@router.callback_query(lambda c: c.data == "reviews")
async def reviews(callback: CallbackQuery) -> None:
    """Display customer reviews."""
    await callback.answer()

    reviews_list = await db.get_reviews()

    if not reviews_list:
        await callback.message.answer(
            "Пока нет отзывов 😢",
            reply_markup=kb.get_back_keyboard()
        )
        return

    media = []

    for review in reviews_list:
        file_id = review["file_id"]
        text = review["text"]

        if file_id:
            caption = text if text else None

            media.append(
                InputMediaPhoto(
                    media=file_id,
                    caption=caption if len(media) == 0 else None
                )
            )

    # Send media in batches (Telegram limit is 10 per group)
    for i in range(0, len(media), 10):
        await callback.message.answer_media_group(media=media[i:i + 10])

    await callback.message.answer(
        "Отзывы клиентов 💬\n"
        "Вы также можете написать отзыв мне в личные сообщения: @Sewwwqp)))",
        reply_markup=kb.get_back_keyboard()
    )


# ======================= CONTACT CALLBACKS =======================

@router.callback_query(lambda c: c.data == "contact_me")
async def contact_me(callback: CallbackQuery) -> None:
    """Display contact information."""
    await callback.answer("Вы выбрали написать мне.")
    await callback.message.answer(
        "Со мной можно связаться вот по этим контактам:\n\n"
        "ТГ-аккаунт: @Sewwwqp\n"
        "Страница Вконтакте: https://vk.com/polya_smi\n"
        "Телеграмм-канал: https://t.me/tortsm\n"
        "Сообщество Вконтакте: https://vk.com/club235221265\n\n"
        "Буду рада помочь Вам!🤗",
        reply_markup=kb.get_back_keyboard()
    )


# ======================= ABOUT CALLBACKS =======================

@router.callback_query(lambda c: c.data == "about")
async def about_callback(callback: CallbackQuery) -> None:
    """Display owner information."""
    await callback.answer("Вы выбрали обо мне.")

    await callback.message.answer_photo(
        photo=OWNER_PHOTO_ID,
        caption=(
            "Привет-привет! Я Полина. Пеку торты не по учебникам, а по любви💗✨\n"
            "А этот бот — мой маленький помощник🤖\n"
            "Первый раз испекла торт больше пяти лет назад — и затянуло😊🍰\n"
            "На заказ работаю около двух лет, и за это время собрала не только навыки, "
            "но и искренние «спасибо».\n"
            "🙏💕\n\n"
            "Хочу, чтобы вкусных тортов в этом мире стало чуть больше\n"
            "И именно ты можешь мне в этом помочь)🍰👩‍🍳"
        ),
        reply_markup=kb.get_back_keyboard()
    )


# ======================= ORDER CREATION CALLBACKS =======================

@router.callback_query(lambda c: c.data == "make_order")
async def make_order(callback: CallbackQuery, state: FSMContext) -> None:
    """Start order creation process."""
    await callback.answer("Вы выбрали сделать заказ.")
    await state.set_state(Form.fullname)
    await callback.message.answer(
        "Давайте создадим заявку Вашего заказа. "
        "Для начала введите Ваше ФИО:",
        reply_markup=kb.get_back_keyboard()
    )


# ======================= CAKE SELECTION CALLBACKS =======================

@router.callback_query(Form.cake, lambda c: c.data.startswith("cake_"))
async def process_cake(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle cake selection."""
    cake_choice = CAKE_NAMES[callback.data]
    await state.update_data(cake=cake_choice)

    await callback.answer()
    await state.set_state(Form.size)
    await callback.message.answer(
        "Теперь выберите размер торта:",
        reply_markup=kb.get_size_choice()
    )


# ======================= SIZE SELECTION CALLBACKS =======================

@router.callback_query(Form.size, lambda c: c.data.startswith("size_"))
async def process_size(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle size selection."""
    size_choice = SIZES[callback.data]
    await state.update_data(size=size_choice)

    await callback.answer()
    await state.set_state(Form.date)
    await callback.message.answer(
        "Выберите дату, к которой нужно приготовить торт:",
        reply_markup=await kb.get_calendar()
    )


# ======================= DATE SELECTION CALLBACKS =======================

@router.callback_query(SimpleCalendarCallback.filter(), Form.date)
async def process_date(
    callback: CallbackQuery,
    callback_data: SimpleCalendarCallback,
    state: FSMContext
) -> None:
    """Handle date selection."""
    selected, date_selected = await SimpleCalendar().process_selection(
        callback,
        callback_data
    )

    if not selected:
        return

    is_valid, message = validator.validate_date(date_selected)

    if not is_valid:
        await callback.answer(message, show_alert=True)
        await callback.message.answer(
            "Выберите дату не менее чем через 3 дня от текущей даты:",
            reply_markup=await kb.get_calendar()
        )
        return

    # Format date
    formatted_date = date_selected.strftime("%d.%m.%Y")

    # Check booking limit
    count = await db.count_orders_by_date(formatted_date)

    if count >= MAX_ORDERS_PER_DATE:
        await callback.answer(
            f"Эта дата уже занята ({MAX_ORDERS_PER_DATE} из {MAX_ORDERS_PER_DATE} заказов)",
            show_alert=True
        )
        await callback.message.answer(
            "Выберите дату в будущем:",
            reply_markup=await kb.get_calendar()
        )
        return

    # Save date
    await state.update_data(date_delivery=formatted_date)
    await state.set_state(Form.logistics)

    await callback.message.answer(
        "Выберите способ доставки:",
        reply_markup=kb.get_logistics_choice()
    )


# ======================= LOGISTICS SELECTION CALLBACKS =======================

@router.callback_query(Form.logistics, lambda c: c.data.startswith("logistics_"))
async def process_logistics(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle delivery method selection."""
    logistics_choice = LOGISTICS[callback.data]
    await state.update_data(logistics=logistics_choice)

    await callback.answer()
    await state.set_state(Form.media)
    await callback.message.answer(
        "Вы можете отправить фото или видео в качестве референса",
        reply_markup=kb.get_miss_keyboard()
    )


# ======================= ORDER CONFIRMATION CALLBACKS =======================

@router.callback_query(lambda c: c.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext) -> None:
    """Confirm and save order."""
    await callback.answer()

    try:
        data = await state.get_data()

        if not data:
            await callback.message.answer("Ошибка: данные заявки пустые")
            return

        await db.add_order(
            telegram_id=callback.from_user.id,
            data=data
        )

        # Prepare order text for admin
        order_text = _format_order_text(data)
        media_type = data.get("media_type")
        media = data.get("media")

        # Send order to admin
        await _send_order_to_admin(callback, order_text, media_type, media)

        await state.clear()

        await callback.message.answer(
            "Заказ принят! Я свяжусь с вами 😊",
            reply_markup=kb.get_back_keyboard()
        )

    except Exception as e:
        print(f"ERROR: {e}")
        await callback.message.answer(
            "Произошла ошибка при создании заказа"
        )


@router.callback_query(lambda c: c.data == "edit_order")
async def edit_order(callback: CallbackQuery, state: FSMContext) -> None:
    """Start order editing process."""
    await callback.answer("Вы выбрали заполнить заявку заново.")
    await callback.message.answer(
        "Давайте начнем заново.\nВведите Ваше ФИО:",
        reply_markup=kb.get_back_keyboard()
    )
    await state.set_state(Form.fullname)


# ======================= HELPER FUNCTIONS =======================

def _format_order_text(data: dict) -> str:
    """Format order data into text message."""
    return (
        "🆕 Новый заказ\n\n"
        f"ФИО: {data['fullname']}\n"
        f"Телефон: {data['phone_number']}\n"
        f"Аккаунт: {data['account']}\n\n"
        f"Торт: {data['cake']}\n"
        f"Размер: {data['size']}\n"
        f"Дата: {data['date_delivery']}\n"
        f"Доставка: {data['logistics']}\n\n"
        f"Дополнительная информация:\n{data['additional_info']}"
    )


async def _send_order_to_admin(
    callback: CallbackQuery,
    order_text: str,
    media_type: str,
    media: str
) -> None:
    """Send order notification to admin."""
    from config.settings import Settings

    admin_id = Settings.ADMIN_ID

    if media_type == "photo":
        await callback.bot.send_photo(
            chat_id=admin_id,
            photo=media,
            caption=order_text
        )
    elif media_type == "video":
        await callback.bot.send_video(
            chat_id=admin_id,
            video=media,
            caption=order_text
        )
    else:
        await callback.bot.send_message(
            chat_id=admin_id,
            text=order_text
        )
