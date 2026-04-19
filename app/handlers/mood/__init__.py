from aiogram import Router

from . import (
    day_change_wish,
    emotions,
    energy,
    main_factor,
    mood_score,
    start,
)

router = Router()

router.include_router(start.router)
router.include_router(mood_score.router)
router.include_router(energy.router)
router.include_router(emotions.router)
router.include_router(main_factor.router)
router.include_router(day_change_wish.router)
