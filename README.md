[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/kOqwghv0)

# ML Project — Предсказание исхода боя в Heroes of Might and Magic III

**Студент:** Слепцова Злата Викторовна

**Группа:** БИВ235


## Оглавление

1. [Описание задачи](#описание-задачи)
2. [Данные](#данные)
3. [Предобработка данных](#предобработка-данных)
4. [Модели](#модели)
5. [Результаты](#результаты)
6. [EDA и визуализации](#eda-и-визуализации)
7. [Структура репозитория](#структура-репозитория)
8. [Запуск проекта](#запуск-проекта)
9. [Воспроизводимость](#воспроизводимость)
10. [Используемые технологии](#используемые-технологии)
11. [Отчёт](#отчёт)


## Описание задачи

Проект посвящён построению симуляционной системы тактических пошаговых боёв и генерации синтетических данных для дальнейшего анализа и машинного обучения.

В рамках проекта реализована упрощённая, но структурно приближенная к оригинальной игре система боя, основанная на механиках Heroes of Might and Magic III.

Цель проекта состоит не в полном воспроизведении игры, а в создании облегчённой модели боя, сохраняющей ключевые игровые зависимости и пригодной для математического моделирования и ML-задач.

Реализованный battle engine включает:
- героев с primary и secondary skills;
- армии из стеков существ;
- дальний и ближний бой;
- систему морали;
- систему удачи;
- расчёт урона;
- пошаговые раунды;
- генерацию синтетических сражений.

**ML-задача:** бинарная классификация — предсказание победителя боя.

**Target:**
- `1` — победа армии A
- `0` — победа армии B


## Репозиторий проекта

https://github.com/hsemlcourse/hseml-group-project-zloilutik-1


## Данные

Датасеты были самостоятельно собраны, очищены и приведены к единому формату для использования в симуляционной модели.

### Использованные датасеты

1. [Heroes III Heroes Dataset](https://www.kaggle.com/datasets/zlata0slepts/heroes-of-might-and-magic-3-heroes)

2. [Heroes III Spells Dataset](https://www.kaggle.com/datasets/zlata0slepts/heroes-of-might-and-magic-3-spells)

3. [Heroes III Skills Dataset](https://www.kaggle.com/datasets/zlata0slepts/heroes-of-might-and-magic-3-skills)

4. [Heroes III War Machines Dataset](https://www.kaggle.com/datasets/zlata0slepts/heroes-of-might-and-magic-3-war-machines)

5. [Heroes III Units Dataset](https://www.kaggle.com/datasets/zlata0slepts/heroes-of-might-and-magic-3-units)

6. [Heroes III Battle Outcome Dataset](https://www.kaggle.com/datasets/zlata0slepts/heroes-iii-battle-outcome-dataset)


### Итоговый battle dataset

Основной ML-датасет был сгенерирован с помощью собственного battle engine.

Размер:
- **10 000 строк**
- **35 колонок**

Примеры признаков:
- характеристики героев;
- secondary skills;
- суммарные характеристики армий;
- количество дальнобойных стеков;
- средняя скорость;
- количество раундов;
- победитель боя.


## Предобработка данных

В preprocessing pipeline входят:
- проверка пропусков;
- проверка дубликатов;
- one-hot encoding категориальных признаков;
- train/validation/test split;
- фиксированный random seed.

Разделение датасета:
- Train — 70%
- Validation — 15%
- Test — 15%

Используемые метрики:
- Accuracy;
- F1-score;
- ROC-AUC.

Основная метрика проекта — **F1-score**.


## Модели

В проекте были обучены и протестированы следующие модели:
- DummyClassifier;
- LogisticRegression;
- KNN;
- RandomForest;
- GradientBoosting;
- ExtraTrees;
- AdaBoost.

Для части моделей выполнялся подбор гиперпараметров с помощью `GridSearchCV`.


## Результаты

Лучшая модель:
- `LogisticRegression`

Результаты на test dataset:

| Метрика | Значение |
|----------|----------|
| Accuracy | 0.941 |
| F1-score | 0.942 |
| ROC-AUC | 0.989 |

Также были проведены эксперименты с:
- ансамблевыми моделями;
- подбором гиперпараметров;
- PCA и уменьшением размерности.


## EDA и визуализации

В проекте реализованы:
- анализ распределения победителей;
- анализ длительности боёв;
- correlation heatmap;
- PCA-визуализация;
- сравнение характеристик армий.

Все графики сохраняются в:

```text
report/images
```


## Структура репозитория

```text
.
├── data
│   ├── processed               # Обработанные датасеты
│   └── raw                     # Исходные датасеты
│
├── report
│   ├── images                  # Графики и визуализации
│   └── report.md               # Финальный отчёт
│
├── src
│   ├── engine
│   │   └── battle_engine.py
│   │
│   ├── models
│   │   ├── unit.py
│   │   ├── hero.py
│   │   └── army.py
│   │
│   ├── systems
│   │   ├── damage.py
│   │   ├── morale.py
│   │   ├── luck.py
│   │   └── battlefield.py
│   │
│   ├── army_generator.py
│   ├── hero_generator.py
│   ├── generate_battles.py
│   ├── preprocessing.py
│   ├── modeling.py
│   ├── eda.py
│   └── dimensionality.py
│
├── tests
│   └── test.py
│
├── requirements.txt
├── pyproject.toml
├── Dockerfile
└── README.md
```


## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/hsemlcourse/hseml-group-project-zloilutik-1.git
cd <repo-name>
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

### 3. Активировать виртуальное окружение

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Установить зависимости

```bash
pip install -r requirements.txt
```

---

### Генерация датасета

```bash
python -m src.generate_battles
```

### Предобработка данных

```bash
python -m src.preprocessing
```

### Обучение моделей

```bash
python -m src.modeling
```

### EDA-анализ

```bash
python -m src.eda
```

### PCA-визуализация

```bash
python -m src.dimensionality
```

### Запуск тестов

```bash
python -m pytest tests/test.py
```


## Воспроизводимость

Проект включает:
- фиксированные random seeds;
- reproducible preprocessing pipeline;
- requirements.txt с фиксированными версиями библиотек;
- Dockerfile;
- Ruff linter configuration.


## Используемые технологии

- Python
- pandas
- scikit-learn
- matplotlib
- pytest
- ruff


## Отчёт

Финальный отчёт:
- `report/report.md`