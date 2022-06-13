from flask import Flask, render_template, request, redirect, url_for

from game.equipment import EquipmentData
from game.personages import personage_classes
from game.utils import load_equipment

app = Flask(__name__)
app.url_map.strict_slashes = False

EQUIPMENT: EquipmentData = load_equipment()

# heroes = {
#     "player": BaseUnit,
#     "enemy": BaseUnit
# }

# arena =  ... # TODO инициализируем класс арены


def render_choose_hero_personage_template(*args, **kwargs) -> str:
    return render_template(
            'hero_choosing.html',
            classes=personage_classes.values(),
            result=EQUIPMENT,
            **kwargs,
        )


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    if request.method == "GET":
        return render_choose_hero_personage_template(
            header='Введите имя героя',
            next_button='Выбрать врага')
    if request.method == "POST":
        pass
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    # TODO кнопка выбор героя. 2 метода GET и POST
    return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    if request.method == "GET":
        return render_choose_hero_personage_template(
            header='Введите врага',
            next_button='Начать сражение')
    if request.method == "POST":
        pass
    return '<h2>Not implemented</h2>'

# @app.route("/fight/")
# def start_fight():
#     # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
#     # TODO рендерим экран боя (шаблон fight.html)
#     pass
#
# @app.route("/fight/hit")
# def hit():
#     # TODO кнопка нанесения удара
#     # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
#     # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
#     # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
#     pass
#
#
# @app.route("/fight/use-skill")
# def use_skill():
#     # TODO кнопка использования скилла
#     # TODO логика пркатикчески идентична предыдущему эндпоинту
#     pass
#
#
# @app.route("/fight/pass-turn")
# def pass_turn():
#     # TODO кнопка пропус хода
#     # TODO логика пркатикчески идентична предыдущему эндпоинту
#     # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
#     pass
#
#
# @app.route("/fight/end-fight")
# def end_fight():
#     # TODO кнопка завершить игру - переход в главное меню
#     return render_template("index.html", heroes=heroes)
#
#

#
#

if __name__ == "__main__":
    app.run()
