from schemas import DietTier, Macros, MealPlan


# ── Tier thresholds ───────────────────────────────────────────────────────────

def get_diet_tier(calories: float) -> DietTier:
    if calories < 100:
        return DietTier.low
    elif calories <= 200:
        return DietTier.medium
    else:
        return DietTier.high


# ── BMR / daily target ────────────────────────────────────────────────────────

def calc_daily_target(
    sex: str,
    age: int,
    height: float,
    weight: float,
    calories_burned: float,
) -> float:
    """
    Harris-Benedict BMR * moderate activity factor + calories burned in session.

    Formula:
        Male   BMR = 88.362 + (13.397 × weight) + (4.799 × height) − (5.677 × age)
        Female BMR = 447.593 + (9.247 × weight) + (3.098 × height) − (4.330 × age)
    Activity factor: 1.55 (moderately active — F1 racer baseline)
    """
    if sex.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    daily = (bmr * 1.55) + calories_burned
    return round(daily, 1)


# ── Macro split for post-session meal ─────────────────────────────────────────

def calc_macros(calories_burned: float, tier: DietTier) -> Macros:
    """
    Post-session meal macros.
    Tier adjusts the carb/protein balance:
      low    → lighter meal (300 kcal target)
      medium → standard recovery (500 kcal target)
      high   → high-energy replenishment (700 kcal target)
    """
    meal_targets = {
        DietTier.low:    300,
        DietTier.medium: 500,
        DietTier.high:   700,
    }
    total = meal_targets[tier]

    # Macro ratios: protein 30% | carbs 45% | fat 25%
    protein_kcal = total * 0.30
    carbs_kcal = total * 0.45
    fat_kcal = total * 0.25

    # Convert to grams (protein 4 kcal/g, carbs 4 kcal/g, fat 9 kcal/g)
    return Macros(
        protein_g=round(protein_kcal / 4, 1),
        carbs_g=round(carbs_kcal / 4, 1),
        fat_g=round(fat_kcal / 9, 1),
        total_kcal=float(total),
    )


# ── Meal recommendations ──────────────────────────────────────────────────────

PRE_SESSION_MEALS = {
    DietTier.low:    "Light snack: 1 banana or a small handful of nuts (30–60 min before)",
    DietTier.medium: "Oat bar + banana with a glass of water (1–2 hrs before)",
    DietTier.high:   "Wholegrain toast with peanut butter + a piece of fruit (2 hrs before)",
}

POST_SESSION_MEALS = {
    DietTier.low: (
        "Light recovery: Greek yoghurt with berries, or a smoothie with "
        "protein powder, banana, and oat milk"
    ),
    DietTier.medium: (
        "Grilled chicken breast (150 g) + white rice (150 g cooked) + "
        "steamed broccoli — consume within 30 min"
    ),
    DietTier.high: (
        "Salmon fillet (200 g) + sweet potato mash + mixed vegetables, "
        "plus a whey protein shake immediately post-session"
    ),
}

ADVICE_TEMPLATES = {
    DietTier.low: (
        "Low-intensity session. Focus on hydration and a light protein snack "
        "within 45 minutes. No major dietary adjustments needed today."
    ),
    DietTier.medium: (
        "Good medium-intensity session. Prioritise carbohydrate replenishment "
        "within 30 minutes to restore glycogen. Include electrolytes if the session "
        "lasted more than 20 minutes."
    ),
    DietTier.high: (
        "High-intensity session — excellent effort! Your muscles need fast-acting "
        "carbohydrates and quality protein immediately. Consume your recovery meal "
        "within 20 minutes and aim for 8+ hours of sleep tonight for optimal recovery."
    ),
}


# ── Hydration estimate ────────────────────────────────────────────────────────

def calc_hydration(duration: float, weight: float) -> int:
    """
    Approximate sweat loss = 0.7–1.0 L per hour, scaled by body weight.
    Returns fluid replacement in ml.
    """
    sweat_rate_per_hour = 0.8 + (weight - 70) * 0.005   # ~0.8 L/hr baseline
    sweat_rate_per_hour = max(0.5, min(sweat_rate_per_hour, 1.5))
    hours = duration / 60
    ml = sweat_rate_per_hour * hours * 1000
    return int(round(ml / 50) * 50)   # round to nearest 50 ml


# ── Main advisor function ─────────────────────────────────────────────────────

def build_meal_plan(
    sex: str,
    age: int,
    height: float,
    weight: float,
    duration: float,
    calories_burned: float,
) -> tuple[DietTier, MealPlan, str]:
    """
    Build a full diet plan from prediction outputs.

    Returns
    -------
    (tier, meal_plan, advice_text)
    """
    tier = get_diet_tier(calories_burned)
    macros = calc_macros(calories_burned, tier)
    daily_target = calc_daily_target(sex, age, height, weight, calories_burned)
    hydration = calc_hydration(duration, weight)

    meal_plan = MealPlan(
        pre_session=PRE_SESSION_MEALS[tier],
        post_session=POST_SESSION_MEALS[tier],
        hydration_ml=hydration,
        daily_target_kcal=daily_target,
        macros=macros,
    )

    advice = ADVICE_TEMPLATES[tier]
    return tier, meal_plan, advice
