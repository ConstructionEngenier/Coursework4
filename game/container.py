from typing import Optional

from game.hero import Enemy, Player


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=SingletonMeta):
    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_processing = False
        self.game_results = ''

    def run(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.game_processing = True

    def _hp_check(self) -> Optional[str]:
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            return self._enf_game(results='В этой битве нет победителя')
        if self.player.hp <= 0:
            return self._enf_game(results=f'{self.enemy.name} победил')
        if self.enemy.hp <= 0:
            return self._enf_game(results=f'{self.player.name} победил')

    def _enf_game(self, results: str):
        self.game_processing = False
        self.game_results = results
        return results

    def next_turn(self) -> str:
        if results := self._hp_check():
            return results

        if not self.game_processing:
            return self.game_results

        results = self.enemy_hit()
        self._stamina_regenerate()
        return results

    def _stamina_regenerate(self):
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()

    def enemy_hit(self) -> str:
        dealt_damage: Optional[float] = self.enemy.hit(self.player)
        if dealt_damage is not None:
            self.player.take_hit(dealt_damage)
            if dealt_damage != 0:
                results = f"{self.enemy.name}, используя {self.enemy.weapon.name}, пробивает {self.player.armor.name}" \
                          f"соперника и наносит {dealt_damage} урона"
            if dealt_damage == 0:
                results = f"{self.enemy.name}, используя {self.enemy.weapon.name}, наносит удар, но " \
                       f"{self.player.armor.name} соперника его останавливает."
        else:
            results = f"{self.enemy.name} попытался использовать {self.enemy.weapon.name}, но у него не хватило " \
                      f"выносливости."
        return results

    def player_hit(self) -> str:
        dealt_damage: Optional[float] = self.player.hit(self.enemy)
        if dealt_damage is not None:
            self.enemy.take_hit(dealt_damage)
            if dealt_damage != 0:
                return f"<p>{self.player.name}, используя {self.player.weapon.name}, пробивает" \
                       f" {self.enemy.armor.name} соперника и наносит {dealt_damage} урона</p><p>{self.next_turn()}</p>"
            else:
                return f"<p>{self.player.name}, используя {self.player.weapon.name}, наносит удар, но " \
                       f"{self.enemy.armor.name} соперника его останавливает.</p><p>{self.next_turn()}</p>"
        return f"<p>{self.player.name} попытался использовать {self.player.weapon.name}, но у него не хватило " \
               f"выносливости.</p><p>{self.next_turn()}</p>"

    def player_use_skill(self) -> str:
        dealt_damage: Optional[float] = self.player.use_skill()
        if dealt_damage is not None:
            self.enemy.take_hit(dealt_damage)
            return f"<p>{self.player.name} использует {self.player.class_.skill.name} и наносит {dealt_damage} урона " \
                   f"сопернику.</p><p>{self.next_turn()}</p>"
        if self.player.skill_used:
            return f"Навык уже использован."
        else:
            return f"<p>{self.player.name} попытался использовать {self.player.class_.skill.name}, но у него не " \
               f"хватило выносливости.</p><p>{self.next_turn()}</p>"
