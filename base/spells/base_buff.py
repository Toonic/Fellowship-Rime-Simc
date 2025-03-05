from base import BaseSpell


class BaseBuff(BaseSpell):
    """Abstract base class for all buffs."""

    remaining_time = 0

    def __init__(self, *args, duration=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = duration
        self.base_tick_rate = duration / self.ticks
        self.tick_rate = 0
        self.time_to_next_tick = 0

        self._is_active = True

    def cast(self, do_damage=False):
        super().cast(do_damage)

    def on_cast_complete(self):
        super().on_cast_complete()
        self.apply_buff()

    def apply_buff(self) -> None:
        """Applies the debuff to the target."""
        self.tick_rate = self.base_tick_rate / (
            1 + (self.character.get_haste() / 100)
        )
        # self.tick_rate = self.base_tick_rate  # Temporary testing against old.
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
        # TODO: Determine if there is a maximum buff/debuff count,
        # and if re-casting it refreshes the duration.

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

    def remove_buff(self) -> None:
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
