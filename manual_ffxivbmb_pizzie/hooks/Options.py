# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, SpecialRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world. 
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# class TotalCharactersToWinWith(Range):
#     """Instead of having to beat the game with all characters, you can limit locations to a subset of character victory locations."""
#     display_name = "Number of characters to beat the game with before victory"
#     range_start = 10
#     range_end = 50
#     default = 50

class PartySize(Choice):
    """
    How many other players in this world will you be able to party up with, it is reccomended you try all duties only with other people trying the challenge.
    [Solo] Just yourself, duties that can't be done solo are filtered out
    [Light Party] 4 players all dungeons.
    [Full Party] 8 players, all dungeons, trials, and raids.
    [Alliance] 24 players, every duty in the game is set as a location.
    """
    display_name = "Party Size"
    option_solo = 0
    option_light_party = 1
    option_full_party = 2
    option_alliance = 3

class DutyDifficulty(Choice):
    """
    Difficulty of the duty content.
    [Normal] Excludes any duty that would take over 30 minutes to complete with the specified party size
    [Hard] Includes the above duties, but excludes extreme/savage duties.
    [Savage] Every duty in the game is included in the location pool with respect to party size.
    """
    display_name = "Duty Difficulty"
    option_normal = 0
    option_hard = 1
    option_savage = 2

class ExpansionGoal(Choice):
    """
    Determines the goal and what expansion content will be put in.
    Certain QoL spells will still be included regardless of choice.
    [ARR] MC #25 is the goal, all level 1-50 content is included.
    [HW] MC #30 is the goal, all level 1-60 content is included.
    [StB] MC #31 is the goal, all level 1-70 content is included.
    [Shb] MC #32 is the goal, all level 1-80 content is included.
    """
    display_name = "Expansion Goal"
    option_arr = 0
    option_hw = 1
    option_stb = 2
    option_shb = 3

class IncludeMainScenario(Choice):
    """
    [No] Excludes the three Main Scenario duties
    [Yes] Includes the three duties
    """
    display_name = "Include Main Scenario Duties"
    option_exclude = 0
    option_include = 1


class GearMode(Choice):
    """
    [Auto] Override any gear/level settings to instead automatically choose splits and increments, these will match the content selection as close as it can
    [Manual] The below settings will take effect
    """
    display_name = "Gearing Mode"
    option_auto = 0
    option_manual = 1

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    #options["total_characters_to_win_with"] = TotalCharactersToWinWith
    options["party_size"] = PartySize
    options["duty_diff"] = DutyDifficulty
    options["expac_goal"] = ExpansionGoal
    options["main_duties"] = IncludeMainScenario

    options["gear_mode"] = GearMode
    
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options