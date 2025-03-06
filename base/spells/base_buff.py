"""Base class for all buffs."""

from rich import print  # pylint: disable=redefined-builtin

from base import BaseSpell


class BaseBuff(BaseSpell):
    """Abstract base class for all buffs."""

    remaining_time = 0

    def __init__(self, *args, duration=0, maximum_stacks=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = duration
        self.base_tick_rate = duration / self.ticks
        self.tick_rate = 0
        self.time_to_next_tick = 0
        self.maximum_stacks = maximum_stacks
        self.current_stacks = 0

        self._is_active = True

    def cast(self, do_damage=False):
        super().cast(do_damage)

    def on_cast_complete(self):
        super().on_cast_complete()
        self.apply_buff()

    def apply_buff(self) -> None:
        """Applies the debuff to the target."""
        if self.simfell_name in self.character.buffs:
            self.character.buffs[self.simfell_name].reapply_buff()
            return

        self.tick_rate = self.base_tick_rate / (
            1 + (self.character.get_haste() / 100)
        )

        self.time_to_next_tick = self.tick_rate
        self.remaining_time = self.duration
        self.character.buffs[self.simfell_name] = self

        self._is_active = True

        if self.character.simulation.do_debug:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + f"✔️ Applied [dark_green]{self.name} "
                + "(Buff)[/dark_green] to character."
            )

    def reapply_buff(self) -> None:
        """Reapplies the buff to the target."""
        if self.current_stacks < self.maximum_stacks:
            self.current_stacks += 1

        self.tick_rate = self.base_tick_rate / (
            1 + (self.character.get_haste() / 100)
        )

        self.time_to_next_tick = self.tick_rate
        self.remaining_time = self.duration
        self.character.buffs[self.simfell_name] = self

        self._is_active = True

        if self.character.simulation.do_debug:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + f"🔄 Re-Applied [dark_green]{self.name} "
                + "(Buff)[/dark_green] to character."
            )

    def update_remaining_duration(self, delta_time: float) -> None:
        """Decreases the remaining buff duration by the delta time."""

        if self._is_active:
            while delta_time > 0 and self.remaining_time > 0:
                if delta_time >= self.time_to_next_tick:
                    self.remaining_time -= self.time_to_next_tick
                    self.time_to_next_tick = self.tick_rate
                    self.on_tick()
                else:
                    self.time_to_next_tick -= delta_time
                    self.remaining_time -= delta_time
                    delta_time = 0

            if self.remaining_time <= 0 and self._is_active:
                self.remove_buff()

    def remove_buff(self, remove_all_stacks=True) -> None:
        """Removes the buff from the character."""

        self.remaining_time = 0
        self.character.buffs.pop(self.simfell_name, None)
        self._is_active = False
        if self.character.simulation.do_debug:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + f"❌ Removed [dark_green]{self.name} "
                + "(Buff)[/dark_green] from character."
            )
