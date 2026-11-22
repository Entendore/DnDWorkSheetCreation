import sys
import os
import json
import random
import html
import math
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QScrollArea,
    QSplitter, QToolBar, QListWidget, QListWidgetItem, QFileDialog,
    QMessageBox, QInputDialog, QMenu, QCompleter, QStatusBar, QDockWidget,
    QSizePolicy, QAbstractItemView
)
from PySide6.QtCore import Qt, QUrl, QTimer, QStandardPaths, QSize
from PySide6.QtGui import (
    QUndoStack, QUndoCommand, QAction, QIcon, QFont, QColor, QPalette,
    QPrinter, QTextDocument
)

# --- DATA CONSTANTS ---
CR_XP = {'0':10,'1/8':25,'1/4':50,'1/2':100,'1':200,'2':450,'3':700,'4':1100,'5':1800,'6':2300,'7':2900,'8':3900,'9':5000,'10':5900,'11':7200,'12':8400,'13':10000,'14':11500,'15':13000,'16':15000,'17':18000,'18':20000,'19':22000,'20':25000,'21':33000,'22':41000,'23':50000,'24':62000,'25':75000,'26':90000,'27':105000,'28':120000,'29':135000,'30':155000}
TYPE_COLORS = {'encounter':'#c0392b','npc':'#2980b9','loot':'#f39c12','session':'#27ae60','backstory':'#8e44ad','quest':'#d35400','faction':'#2c3e50','spellbook':'#6c3483'}
MONS = [m.split('|') for m in 'Goblin|7|15|1/4,Skeleton|13|13|1/4,Zombie|22|8|1/4,Bandit|11|12|1/8,Giant Rat|7|12|1/8,Kobold|5|12|1/8,Wolf|11|13|1/4,Orc|15|13|1/2,Bugbear|27|16|1,Ghoul|22|12|1,Shadow|16|12|1/2,Ogre|59|11|2,Troll|84|15|5,Mimic|58|12|2,Young Black Dragon|127|18|7,Mind Flayer|71|15|7,Beholder|180|18|13,Lich|135|17|21,Wraith|67|13|5,Will-o\'-Wisp|22|19|2,Giant Spider|26|14|1,Hobgoblin|11|18|1/2,Guard|11|16|1/8,Acolyte|9|10|1/8,Cultist|9|12|1/8,Scout|11|13|1/2,Thug|32|11|1/2,Boar|11|12|1/4,Centaur|45|12|2,Darkmantle|22|13|1/2,Gargoyle|52|15|2,Green Hag|82|17|3,Harpy|38|11|1,Minotaur|76|14|3,Owlbear|59|13|3'.split(',')]
SPELLS = [s.split('|') for s in 'Fire Bolt|Cantrip|Evocation,Light|Cantrip|Evocation,Mage Hand|Cantrip|Conjuration,Prestidigitation|Cantrip|Transmutation,Sacred Flame|Cantrip|Evocation,Toll the Dead|Cantrip|Necromancy,Guidance|Cantrip|Divination,Minor Illusion|Cantrip|Illusion,Message|Cantrip|Transmutation,Chill Touch|Cantrip|Necromancy,Ray of Frost|Cantrip|Evocation,Druidcraft|Cantrip|Transmutation,Thaumaturgy|Cantrip|Evocation,Acid Splash|Cantrip|Conjuration,Shield|1st|Abjuration,Healing Word|1st|Evocation,Cure Wounds|1st|Evocation,Bless|1st|Enchantment,Sleep|1st|Enchantment,Detect Magic|1st|Divination,Magic Missile|1st|Evocation,Thunderwave|1st|Evocation,Burning Hands|1st|Evocation,Faerie Fire|1st|Enchantment,Hex|1st|Enchantment,Entangle|1st|Conjuration,Speak with Animals|1st|Divination,Misty Step|2nd|Conjuration,Invisibility|2nd|Illusion,Hold Person|2nd|Enchantment,Shatter|2nd|Evocation,Scorching Ray|2nd|Evocation,Web|2nd|Conjuration,Silence|2nd|Illusion,Spiritual Weapon|2nd|Evocation,Enhance Ability|2nd|Transmutation,Blindness/Deafness|2nd|Necromancy,Suggestion|2nd|Enchantment,Darkness|2nd|Evocation,Spider Climb|2nd|Transmutation,Moonbeam|2nd|Evocation,Flaming Sphere|2nd|Conjuration,Aid|2nd|Abjuration,Fireball|3rd|Evocation,Counterspell|3rd|Abjuration,Dispel Magic|3rd|Abjuration,Lightning Bolt|3rd|Evocation,Spirit Guardians|3rd|Conjuration,Revivify|3rd|Necromancy,Fly|3rd|Transmutation,Haste|3rd|Transmutation,Slow|3rd|Transmutation,Hypnotic Pattern|3rd|Illusion,Fear|3rd|Illusion,Beacon of Hope|3rd|Abjuration,Animate Dead|3rd|Necromancy,Polymorph|4th|Transmutation,Greater Invisibility|4th|Illusion,Banishment|4th|Abjuration,Dimension Door|4th|Conjuration,Fire Shield|4th|Evocation,Ice Storm|4th|Evocation,Stoneskin|4th|Abjuration,Wall of Fire|4th|Evocation,Blight|4th|Necromancy,Confusion|4th|Enchantment,Freedom of Movement|4th|Abjuration,Teleport|7th|Conjuration,Greater Restoration|5th|Abjuration,Mass Cure Wounds|5th|Evocation,Cone of Cold|5th|Evocation,Wall of Force|5th|Evocation,Hold Monster|5th|Enchantment,Scrying|5th|Divination,Destructive Wave|5th|Necromancy,Flame Strike|5th|Evocation,Geas|5th|Enchantment,Heal|6th|Necromancy,Disintegrate|6th|Transmutation,Globe of Invulnerability|6th|Abjuration,Sunburst|6th|Evocation,Chain Lightning|6th|Evocation,True Seeing|6th|Divination,Word of Recall|6th|Conjuration,Harm|6th|Necromancy,Power Word Kill|8th|Enchantment,Maze|8th|Conjuration,Dominate Monster|8th|Enchantment,Incendiary Cloud|8th|Conjuration,Earthquake|8th|Evolution,Antimagic Field|8th|Abjuration,Meteor Swarm|9th|Evolution,Time Ravage|9th|Necromancy,Wish|9th|Conjuration,True Polymorph|9th|Transmutation,Power Word Heal|9th|Evolution,Gate|9th|Conjuration,Foresight|9th|Divination'.split(',')]
RN = {
    'first': ['Aelara','Braxus','Caelia','Durnik','Elara','Fendrel','Gwendolyn','Haldric','Isolde','Jareth','Kaelen','Lirien','Morgrim','Nerys','Orvyn','Pyrrhus','Quinara','Roderic','Sylas','Thalia','Ulric','Vespera','Warrick','Xara','Ysolde','Zareth','Brynn','Callum','Daria','Emeric'],
    'last': ['Ashwood','Blackthorn','Coppervein','Dawnblade','Emberfall','Frostweaver','Goldleaf','Hawkwind','Ironheart','Jade','Kindlecrag','Lightbringer','Moonshadow','Nightbreeze','Oakenshield','Proudfoot','Quicksilver','Ravencrest','Silvermane','Thornwall','Underbough','Viper','Windrunner','Stormborn','Duskwalker','Brightwater','Crimson','Fellhammer','Grimshaw','Holloway'],
    'traits': ['Speaks in riddles','Unfailingly polite even when angry','Always hungry','Paranoid about being watched','Collects unusual trinkets','Laughs at inappropriate moments','Speaks very slowly','Constantly fidgeting with a coin','Refuses to make eye contact','Overly dramatic','Whispers even in quiet rooms','Uses overly formal language','Sniffs the air frequently','Taps fingers in complex rhythms','Refers to self in third person'],
    'ideals': ['Freedom — chains must be broken','Knowledge — truth at any price','Power — the strong guide the weak','Charity — help those in need','Balance — all things in harmony','Vengeance — wrongs must be answered','Tradition — the old ways are best','Creativity — beauty elevates life'],
    'secrets': ['Is actually a shapechanger','Owes a massive debt to a crime syndicate','Child of a powerful fiend','Secretly poisoning a water supply','Searching for a way to resurrect a loved one','Knows the location of a powerful artifact','Was once a famous hero who faked their death','Being blackmailed by a rival'],
    'manns': ['Whispers even when speaking normally','Uses archaic language','Sniffs the air while talking','Taps fingers in complex rhythms','Refers to self in third person','Ends sentences with "...or so they say"','Pauses dramatically before key words','Accidentally rhymes and gets embarrassed','Clicks tongue between sentences','Writes in the air while speaking']
}

TYPES = {
    'encounter': {'label': 'Encounter', 'icon': '💀', 'desc': 'Plan combat encounters with monsters, tactics, XP budgeting, and loot.', 'fields': [
        {'k': 'name', 'l': 'Encounter Name', 't': 'text', 'p': 'e.g. Ambush at the Crossroads'},
        {'k': 'cr', 'l': 'Challenge Rating', 't': 'text', 'p': 'e.g. 3 or 1/2'},
        {'k': 'environment', 'l': 'Environment', 't': 'select', 'o': ['Forest','Dungeon','Cave','Swamp','Mountain','Desert','Urban','Coastal','Underdark','Feywild','Shadowfell','Other Plane','Other']},
        {'k': 'partyLevel', 'l': 'Party Level', 't': 'number', 'p': '5'},
        {'k': 'partySize', 'l': 'Party Size', 't': 'number', 'p': '4'},
        {'type': 'dyn', 'k': 'monsters', 'l': 'Monsters', 'fields': [
            {'k': 'name', 'l': 'Name', 't': 'text', 'p': 'Goblin'}, {'k': 'qty', 'l': 'Qty', 't': 'number', 'p': '1', 'w': 50},
            {'k': 'hp', 'l': 'HP', 't': 'text', 'p': '7'}, {'k': 'ac', 'l': 'AC', 't': 'text', 'p': '15'},
            {'k': 'cr', 'l': 'CR', 't': 'text', 'p': '1/4', 'w': 50}, {'k': 'init', 'l': 'Init', 't': 'text', 'p': '', 'w': 45}, {'k': 'notes', 'l': 'Notes', 't': 'text', 'p': ''}
        ], 'quickAdd': True},
        {'k': 'tactics', 'l': 'Tactics & Strategy', 't': 'textarea', 'p': 'Describe how the enemies fight...'},
        {'k': 'loot', 'l': 'Loot Dropped', 't': 'textarea', 'p': 'List any treasure or items...'},
        {'k': 'notes', 'l': 'DM Notes', 't': 'textarea', 'p': 'Additional notes for yourself...'}
    ]},
    'npc': {'label': 'NPC', 'icon': '🛡️', 'desc': 'Create detailed NPCs with personality, secrets, and stat blocks.', 'fields': [
        {'k': 'name', 'l': 'Name', 't': 'text', 'p': 'e.g. Elara Moonwhisper'}, {'k': 'raceClass', 'l': 'Race & Class', 't': 'text', 'p': 'e.g. Half-Elf Bard'},
        {'k': 'alignment', 'l': 'Alignment', 't': 'select', 'o': ['Lawful Good','Neutral Good','Chaotic Good','Lawful Neutral','True Neutral','Chaotic Neutral','Lawful Evil','Neutral Evil','Chaotic Evil']},
        {'k': 'age', 'l': 'Age', 't': 'text', 'p': 'e.g. 142'}, {'k': 'personalityTraits', 'l': 'Personality Traits', 't': 'textarea', 'p': 'I am... I also...'},
        {'k': 'ideal', 'l': 'Ideal', 't': 'textarea', 'p': 'What drives this NPC?'}, {'k': 'bond', 'l': 'Bond', 't': 'textarea', 'p': 'Who or what are they connected to?'},
        {'k': 'flaw', 'l': 'Flaw', 't': 'textarea', 'p': 'What is their weakness?'}, {'k': 'appearance', 'l': 'Physical Description', 't': 'textarea', 'p': 'Describe their appearance...'},
        {'k': 'mannerisms', 'l': 'Speaking Mannerisms', 't': 'textarea', 'p': 'How do they talk?'}, {'k': 'secret', 'l': 'Secret', 't': 'textarea', 'p': 'What are they hiding?'},
        {'k': 'statBlock', 'l': 'Stat Block Summary', 't': 'textarea', 'p': 'Key stats, abilities, spells...'}
    ]},
    'loot': {'label': 'Loot Table', 'icon': '💎', 'desc': 'Build random loot tables for rolling treasure.', 'fields': [
        {'k': 'name', 'l': 'Table Name', 't': 'text', 'p': 'e.g. Goblin Horde Loot'},
        {'k': 'rollType', 'l': 'Roll Type', 't': 'select', 'o': ['d4','d6','d8','d10','d12','d20','d100']},
        {'type': 'dyn', 'k': 'rows', 'l': 'Table Entries', 'fields': [
            {'k': 'range', 'l': 'Range', 't': 'text', 'p': '1-5', 'w': 65}, {'k': 'item', 'l': 'Item', 't': 'text', 'p': '2d6 gold pieces'},
            {'k': 'qty', 'l': 'Qty', 't': 'text', 'p': '', 'w': 45}, {'k': 'notes', 'l': 'Notes', 't': 'text', 'p': ''}
        ]}
    ]},
    'session': {'label': 'Session Notes', 'icon': '📜', 'desc': 'Record session details, events, and follow-up hooks.', 'fields': [
        {'k': 'number', 'l': 'Session Number', 't': 'text', 'p': 'e.g. 12'}, {'k': 'date', 'l': 'Date', 't': 'text', 'p': 'e.g. March 15, 2025'},
        {'k': 'location', 'l': 'Location / Region', 't': 'text', 'p': 'e.g. The Underdark'}, {'k': 'players', 'l': 'Players Present', 't': 'textarea', 'p': 'List who was at the table...'},
        {'k': 'keyEvents', 'l': 'Key Events', 't': 'textarea', 'p': 'What happened this session...'}, {'k': 'npcsEncountered', 'l': 'NPCs Encountered', 't': 'textarea', 'p': 'Notable NPCs...'},
        {'k': 'combats', 'l': 'Combat Encounters', 't': 'textarea', 'p': 'Summarize each fight...'}, {'k': 'cliffhanger', 'l': 'Cliffhanger / Next Hook', 't': 'textarea', 'p': 'What will hook them next time...'},
        {'k': 'xp', 'l': 'XP Awarded', 't': 'text', 'p': 'e.g. 450'}, {'k': 'goldLoot', 'l': 'Gold & Loot Found', 't': 'textarea', 'p': 'List treasure acquired...'},
        {'k': 'notes', 'l': 'DM Notes', 't': 'textarea', 'p': 'Reminders for next session...'}
    ]},
    'backstory': {'label': 'Backstory', 'icon': '📖', 'desc': 'Write rich character backstories with bonds, flaws, and goals.', 'fields': [
        {'k': 'name', 'l': 'Character Name', 't': 'text', 'p': 'e.g. Thorin Ironfist'},
        {'k': 'race', 'l': 'Race', 't': 'select', 'o': ['Human','Elf','Dwarf','Halfling','Gnome','Half-Elf','Half-Orc','Tiefling','Dragonborn','Aasimar','Firbolg','Goliath','Kenku','Tabaxi','Triton','Genasi','Other']},
        {'k': 'class', 'l': 'Class', 't': 'select', 'o': ['Artificer','Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard']},
        {'k': 'background', 'l': 'Background', 't': 'select', 'o': ['Acolyte','Charlatan','Criminal','Entertainer','Folk Hero','Guild Artisan','Hermit','Noble','Outlander','Sage','Sailor','Soldier','Urchin','Other']},
        {'k': 'level', 'l': 'Level', 't': 'text', 'p': 'e.g. 3'}, {'k': 'personalityTraits', 'l': 'Personality Traits', 't': 'textarea', 'p': 'I am... I also...'},
        {'k': 'ideal', 'l': 'Ideal', 't': 'textarea', 'p': 'What does your character believe in?'}, {'k': 'bond', 'l': 'Bond', 't': 'textarea', 'p': 'Who connects them to the world?'},
        {'k': 'flaw', 'l': 'Flaw', 't': 'textarea', 'p': 'Greatest weakness?'}, {'k': 'backstory', 'l': 'Backstory', 't': 'textarea', 'p': 'Tell their story...'},
        {'k': 'goals', 'l': 'Goals & Ambitions', 't': 'textarea', 'p': 'What do they want?'}, {'k': 'relationships', 'l': 'Relationships', 't': 'textarea', 'p': 'Family, friends, enemies...'},
        {'k': 'heirlooms', 'l': 'Special Items & Heirlooms', 't': 'textarea', 'p': 'Possessions with sentimental value...'}
    ]},
    'quest': {'label': 'Quest', 'icon': '🗺️', 'desc': 'Design quest hooks with objectives, rewards, and twists.', 'fields': [
        {'k': 'name', 'l': 'Quest Name', 't': 'text', 'p': 'e.g. The Lost Crown of Ashenmoor'}, {'k': 'giver', 'l': 'Quest Giver', 't': 'text', 'p': 'e.g. Councilwoman Hestra'},
        {'k': 'location', 'l': 'Location', 't': 'text', 'p': 'e.g. The Ruins of Ashenmoor'}, {'k': 'levelRange', 'l': 'Recommended Level', 't': 'text', 'p': 'e.g. 3-5'},
        {'k': 'questType', 'l': 'Quest Type', 't': 'select', 'o': ['Main Plot','Side Quest','One-Shot','Multi-Part','Dungeon Delve','Investigation','Escort','Fetch','Assassination','Diplomatic','Other']},
        {'type': 'dyn', 'k': 'objectives', 'l': 'Objectives', 'fields': [{'k': 'text', 'l': 'Objective', 't': 'text', 'p': 'Find the entrance'}]},
        {'k': 'rewards', 'l': 'Rewards', 't': 'textarea', 'p': 'Gold, items, reputation...'}, {'k': 'complications', 'l': 'Complications', 't': 'textarea', 'p': 'What can go wrong?'},
        {'k': 'npcsInvolved', 'l': 'Key NPCs', 't': 'textarea', 'p': 'Allies, enemies, neutrals...'}, {'k': 'twist', 'l': 'Secret Twist', 't': 'textarea', 'p': 'The unexpected turn...'},
        {'k': 'notes', 'l': 'DM Notes', 't': 'textarea', 'p': 'Prep notes...'}
    ]},
    'faction': {'label': 'Faction', 'icon': '🏛️', 'desc': 'Organize factions with leadership, goals, alliances, and politics.', 'fields': [
        {'k': 'name', 'l': 'Faction Name', 't': 'text', 'p': 'e.g. The Silver Covenant'},
        {'k': 'factionType', 'l': 'Type', 't': 'select', 'o': ['Guild','Cult','Government','Military','Criminal Syndicate','Religious Order','Mercenary Company','Merchant League','Secret Society','Tribal','Other']},
        {'k': 'alignment', 'l': 'Alignment', 't': 'select', 'o': ['Lawful Good','Neutral Good','Chaotic Good','Lawful Neutral','True Neutral','Chaotic Neutral','Lawful Evil','Neutral Evil','Chaotic Evil']},
        {'k': 'leader', 'l': 'Leader', 't': 'text', 'p': 'e.g. High Priestess Valera'}, {'k': 'hq', 'l': 'Headquarters', 't': 'text', 'p': 'e.g. The Sunken Temple'},
        {'k': 'members', 'l': 'Estimated Members', 't': 'text', 'p': 'e.g. ~200'}, {'k': 'resources', 'l': 'Resources & Assets', 't': 'textarea', 'p': 'Wealth, strongholds...'},
        {'k': 'goals', 'l': 'Goals', 't': 'textarea', 'p': 'What do they want?'}, {'k': 'methods', 'l': 'Methods', 't': 'textarea', 'p': 'How do they operate?'},
        {'k': 'allies', 'l': 'Allies', 't': 'textarea', 'p': 'Who supports them?'}, {'k': 'enemies', 'l': 'Enemies', 't': 'textarea', 'p': 'Who opposes them?'},
        {'k': 'secrets', 'l': 'Inner Secrets', 't': 'textarea', 'p': "What don't outsiders know?"},
        {'type': 'dyn', 'k': 'notableMembers', 'l': 'Notable Members', 'fields': [
            {'k': 'name', 'l': 'Name', 't': 'text', 'p': 'Name'}, {'k': 'role', 'l': 'Role', 't': 'text', 'p': 'Role', 'w': 100}, {'k': 'notes', 'l': 'Notes', 't': 'text', 'p': ''}
        ]}
    ]},
    'spellbook': {'label': 'Spellbook', 'icon': '🧙', 'desc': 'Track known spells, spell slots, and prepare for sessions.', 'fields': [
        {'k': 'name', 'l': 'Character Name', 't': 'text', 'p': 'e.g. Zephyra the Wise'},
        {'k': 'spellClass', 'l': 'Class', 't': 'select', 'o': ['Artificer','Bard','Cleric','Druid','Paladin','Ranger','Sorcerer','Warlock','Wizard']},
        {'k': 'spellDC', 'l': 'Spell Save DC', 't': 'text', 'p': 'e.g. 15'}, {'k': 'spellAtk', 'l': 'Spell Attack Modifier', 't': 'text', 'p': 'e.g. +7'},
        {'type': 'dyn', 'k': 'spellSlots', 'l': 'Spell Slots', 'fields': [
            {'k': 'level', 'l': 'Level', 't': 'text', 'p': '1st', 'w': 45}, {'k': 'total', 'l': 'Total', 't': 'number', 'p': '4', 'w': 45}, {'k': 'used', 'l': 'Used', 't': 'number', 'p': '0', 'w': 45}
        ]},
        {'type': 'dyn', 'k': 'spells', 'l': 'Known Spells', 'fields': [
            {'k': 'name', 'l': 'Spell Name', 't': 'text', 'p': 'Fireball', 'autocomplete': 'spell'}, {'k': 'level', 'l': 'Lvl', 't': 'text', 'p': '3rd', 'w': 45},
            {'k': 'school', 'l': 'School', 't': 'text', 'p': 'Evocation', 'w': 85}, {'k': 'notes', 'l': 'Notes', 't': 'text', 'p': ''}
        ]}
    ]}
}

def get_defaults():
    return {
        'encounter': {'name':'','cr':'','environment':'Forest','partyLevel':5,'partySize':4,'monsters':[{'name':'','qty':1,'hp':'','ac':'','cr':'','init':'','notes':''}],'tactics':'','loot':'','notes':''},
        'npc': {'name':'','raceClass':'','alignment':'True Neutral','age':'','personalityTraits':'','ideal':'','bond':'','flaw':'','appearance':'','mannerisms':'','secret':'','statBlock':''},
        'loot': {'name':'','rollType':'d20','rows':[{'range':'','item':'','qty':'','notes':''}]},
        'session': {'number':'','date':'','location':'','players':'','keyEvents':'','npcsEncountered':'','combats':'','cliffhanger':'','xp':'','goldLoot':'','notes':''},
        'backstory': {'name':'','race':'Human','class':'Fighter','background':'Folk Hero','level':'','personalityTraits':'','ideal':'','bond':'','flaw':'','backstory':'','goals':'','relationships':'','heirlooms':''},
        'quest': {'name':'','giver':'','location':'','levelRange':'','questType':'Side Quest','objectives':[{'text':''}],'rewards':'','complications':'','npcsInvolved':'','twist':'','notes':''},
        'faction': {'name':'','factionType':'Guild','alignment':'True Neutral','leader':'','hq':'','members':'','resources':'','goals':'','methods':'','allies':'','enemies':'','secrets':'','notableMembers':[{'name':'','role':'','notes':''}]},
        'spellbook': {'name':'','spellClass':'Wizard','spellDC':'','spellAtk':'','spellSlots':[{'level':'1st','total':4,'used':0},{'level':'2nd','total':3,'used':0},{'level':'3rd','total':2,'used':0}],'spells':[{'name':'','level':'Cantrip','school':'','notes':''}]}
    }

# --- HELPERS ---
def esc(s): return html.escape(str(s or ''))
def adj_m(n): return 1 if n==1 else 1.5 if n==2 else 2 if n<=6 else 2.5 if n<=10 else 3 if n<=14 else 4
def get_thresh(lv, sz): return {'easy':lv*25*sz, 'medium':lv*50*sz, 'hard':lv*75*sz, 'deadly':lv*150*sz}
def fmt_n(n): return f"{n:,}"
def make_dice_html(text):
    import re
    def repl(m): 
        n, s, mod = m.group(1) or '1', m.group(2), m.group(3) or '0'
        return f'<a href="dice://{n}/{s}/{mod}" style="color:#8b7355; text-decoration: none; border-bottom: 1.5px dashed #8b7355; font-weight:600; cursor:pointer;">{m.group(0)}</a>'
    return re.sub(r'(\d*)d(\d+)([+-]\d+)?', repl, esc(text))

def calc_xp(d):
    if not d.get('partyLevel') or not d.get('partySize'): return None
    lv, sz = int(d['partyLevel']) or 1, int(d['partySize']) or 4
    total, mc = 0, 0
    for m in d.get('monsters', []):
        if m.get('name') and m.get('cr'):
            total += CR_XP.get(m['cr'], 0) * (int(m.get('qty') or 1))
            mc += int(m.get('qty') or 1)
    mult = adj_m(mc)
    adj = int(total * mult)
    th = get_thresh(lv, sz)
    diff, color, pct = 'Trivial', '#7a8a6e', 5
    if adj >= th['deadly']: diff, color, pct = 'Deadly', '#b83a3a', 100
    elif adj >= th['hard']: diff, color, pct = 'Hard', '#d46b2a', 60 + 40*((adj-th['hard'])/(th['deadly']-th['hard'] or 1))
    elif adj >= th['medium']: diff, color, pct = 'Medium', '#c9952d', 30 + 30*((adj-th['medium'])/(th['hard']-th['medium'] or 1))
    elif adj >= th['easy']: diff, color, pct = 'Easy', '#5a9e3e', 10 + 20*((adj-th['easy'])/(th['medium']-th['easy'] or 1))
    suggest = ''
    if mc > 0:
        if diff == 'Deadly' and mc <= 3: suggest = 'Consider removing a monster or lowering a CR.'
        elif diff == 'Deadly': suggest = 'Very dangerous. Consider splitting into multiple encounters.'
        elif diff == 'Trivial': suggest = 'Too easy for this party.'
        elif diff == 'Easy': suggest = 'A warm-up fight.'
        elif diff == 'Medium': suggest = 'A solid challenge for a standard encounter.'
        elif diff == 'Hard': suggest = 'Tough but fair. Party may need to use resources.'
    return {'adj':adj, 'mc':mc, 'diff':diff, 'color':color, 'pct':min(100,pct), 'th':th, 'lv':lv, 'sz':sz, 'suggest':suggest}

def pv_section(title, content, raw=False):
    if not content or not content.strip(): return ''
    c = esc(content) if raw else make_dice_html(content)
    return f'<div class="ws"><h2 class="wst">{esc(title)}</h2><p class="wtx">{c}</p></div>'

def get_preview_css(dark=False):
    if dark:
        return "body{background:#1a1815;color:#e8dcc8;font-family:'Segoe UI',Tahoma,sans-serif;margin:0;padding:0}a{color:#c9952d}.wp{background:#1a1815;border:2px solid #3a352e;padding:1.4rem 1.2rem;box-shadow:0 2px 10px rgba(0,0,0,.3);position:relative;max-width:700px;margin:0 auto}.wp::before{content:'';position:absolute;inset:4px;border:1px solid rgba(201,149,45,.12);pointer-events:none}.wh{text-align:center;border-bottom:2px double rgba(201,149,45,.3);padding-bottom:.7rem;margin-bottom:.9rem}.wtl{font-size:.6rem;letter-spacing:.3em;color:#c9952d;text-transform:uppercase}.wtt{font-size:1.25rem;font-weight:700;color:#e8dcc8;margin:.2rem 0}.wm{font-size:.8rem;color:#8a7e6b}.ws{margin-bottom:.9rem}.wst{font-size:.65rem;letter-spacing:.1em;color:#c9952d;text-transform:uppercase;border-bottom:1px solid #2e2a23;padding-bottom:.12rem;margin-bottom:.4rem;font-weight:600}.wt{width:100%;border-collapse:collapse;font-size:.8rem;margin-bottom:.5rem}.wt th,.wt td{border:1px solid #2e2a23;padding:.2rem .4rem;text-align:left}.wt th{background:#242119;color:#e8dcc8;font-size:.6rem;text-transform:uppercase;letter-spacing:.03em}.wtx{white-space:pre-wrap;font-size:.85rem;line-height:1.5;color:#c4b89a}.wfr{display:flex;gap:.6rem;margin-bottom:.3rem}.wf{flex:1}.wfl{font-size:.6rem;color:#c9952d;text-transform:uppercase;letter-spacing:.08em}.wfv{font-size:.9rem}.wd{margin:.7rem 0}.wd-label{font-size:.65rem;color:#c9952d;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.15rem}.wd-track{height:5px;background:#242119;border-radius:3px;overflow:hidden}.wd-fill{height:100%;border-radius:3px}.wd-xp{font-size:.7rem;color:#8a7e6b;margin-top:.15rem}.wd-suggest{font-size:.75rem;margin-top:.25rem;padding:.2rem .35rem;border-left:3px solid;color:#8a7e6b}.obj-row{display:flex;align-items:flex-start;gap:.35rem;margin-bottom:.25rem;font-size:.85rem}.obj-chk{width:13px;height:13px;border:1.5px solid #2e2a23;border-radius:2px;flex-shrink:0;margin-top:2px}.mem-card{border:1px solid #2e2a23;border-radius:.2rem;padding:.35rem;margin-bottom:.3rem;background:rgba(201,149,45,.03)}.mem-name{font-weight:700;font-size:.85rem}.mem-role{font-size:.75rem;color:#8a7e6b;font-style:italic}.slot-row{display:flex;align-items:center;gap:.3rem;margin-bottom:.25rem}.slot-label{font-size:.8rem;width:45px}.slots{display:flex;gap:2px}.slot{width:14px;height:14px;border-radius:50%;border:1.5px solid #2e2a23;background:transparent}.slot.used{background:rgba(201,149,45,.2);border-color:#c9952d}.dice-btn{display:inline-flex;align-items:center;gap:.3rem;padding:.3rem .6rem;border:2px solid #2e2a23;border-radius:.25rem;background:#242119;color:#e8dcc8;font-size:.7rem;text-transform:uppercase;cursor:pointer;text-decoration:none;margin:.35rem 0}.dice-btn:hover{background:rgba(201,149,45,.15);border-color:#c9952d}.roll-result{display:inline-block;padding:.1rem .4rem;border-radius:.2rem;font-weight:700;margin-left:.3rem}.row-hl{background:rgba(201,149,45,.2)!important}"
    return "body{background:#f0e6d0;color:#2c1810;font-family:'Segoe UI',Tahoma,sans-serif;margin:0;padding:0}a{color:#5a4030}.wp{background:#f0e6d0;border:2px solid #8b7355;padding:1.4rem 1.2rem;box-shadow:0 2px 10px rgba(0,0,0,.1);position:relative;background-image:radial-gradient(ellipse at 20% 80%,rgba(139,115,85,.08) 0%,transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(139,115,85,.06) 0%,transparent 50%);max-width:700px;margin:0 auto}.wp::before{content:'';position:absolute;inset:4px;border:1px solid rgba(139,115,85,.25);pointer-events:none}.wh{text-align:center;border-bottom:2px double #8b7355;padding-bottom:.7rem;margin-bottom:.9rem}.wtl{font-size:.55rem;letter-spacing:.3em;color:#8b7355;text-transform:uppercase}.wtt{font-size:1.25rem;font-weight:700;color:#2c1810;margin:.2rem 0}.wm{font-size:.8rem;color:#5a4030}.ws{margin-bottom:.9rem}.wst{font-size:.65rem;letter-spacing:.1em;color:#8b7355;text-transform:uppercase;border-bottom:1px solid #c4a882;padding-bottom:.12rem;margin-bottom:.4rem;font-weight:600}.wt{width:100%;border-collapse:collapse;font-size:.8rem;margin-bottom:.5rem}.wt th,.wt td{border:1px solid #c4a882;padding:.2rem .4rem;text-align:left}.wt th{background:#e6d5b8;font-size:.6rem;text-transform:uppercase;letter-spacing:.03em}.wtx{white-space:pre-wrap;font-size:.85rem;line-height:1.5}.wfr{display:flex;gap:.6rem;margin-bottom:.3rem}.wf{flex:1}.wfl{font-size:.6rem;color:#8b7355;text-transform:uppercase;letter-spacing:.08em}.wfv{font-size:.9rem}.wd{margin:.7rem 0}.wd-label{font-size:.65rem;color:#8b7355;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.15rem}.wd-track{height:5px;background:#d4c4a8;border-radius:3px;overflow:hidden}.wd-fill{height:100%;border-radius:3px}.wd-xp{font-size:.7rem;color:#5a4030;margin-top:.15rem}.wd-suggest{font-size:.75rem;margin-top:.25rem;padding:.2rem .35rem;border-left:3px solid;color:#5a4030}.obj-row{display:flex;align-items:flex-start;gap:.35rem;margin-bottom:.25rem;font-size:.85rem}.obj-chk{width:13px;height:13px;border:1.5px solid #8b7355;border-radius:2px;flex-shrink:0;margin-top:2px}.mem-card{border:1px solid #c4a882;border-radius:.2rem;padding:.35rem;margin-bottom:.3rem;background:rgba(196,168,130,.06)}.mem-name{font-weight:700;font-size:.85rem}.mem-role{font-size:.75rem;color:#5a4030;font-style:italic}.slot-row{display:flex;align-items:center;gap:.3rem;margin-bottom:.25rem}.slot-label{font-size:.8rem;width:45px}.slots{display:flex;gap:2px}.slot{width:14px;height:14px;border-radius:50%;border:1.5px solid #8b7355;background:transparent}.slot.used{background:#8b7355}.dice-btn{display:inline-flex;align-items:center;gap:.3rem;padding:.3rem .6rem;border:2px solid #8b7355;border-radius:.25rem;background:#e6d5b8;color:#2c1810;font-size:.7rem;text-transform:uppercase;cursor:pointer;text-decoration:none;margin:.35rem 0}.dice-btn:hover{background:#8b7355;color:#fff}.roll-result{display:inline-block;padding:.1rem .4rem;border-radius:.2rem;font-weight:700;margin-left:.3rem}.row-hl{background:rgba(201,149,45,.25)!important}"

def empty_pv(css): return f'<div class="wp" style="text-align:center;padding:2rem"><div class="wtl" style="margin-bottom:.6rem">Worksheet Preview</div><p style="color:#b0a08a;font-style:italic">Start filling in the form to see your worksheet.</p></div>'

def gen_html(d, wtype, dark=False):
    css = get_preview_css(dark)
    has_content = d.get('name') or d.get('cr') or any(m.get('name') for m in d.get('monsters',[])) if wtype=='encounter' else d.get('name') or d.get('giver') if wtype=='quest' else d.get('name')
    if not has_content: return f"<html><head><style>{css}</style></head><body>{empty_pv(css)}</body></html>"
    
    body = ""
    if wtype == 'encounter':
        xp = calc_xp(d)
        mons = ""
        m_list = sorted([m for m in d.get('monsters',[]) if m.get('name')], key=lambda x: int(x.get('init') or 0), reverse=True)
        if m_list:
            mons = f'<div class="ws"><h2 class="wst">Monsters {"(by Initiative)" if any(m.get("init") for m in d["monsters"]) else ""}</h2><table class="wt"><tr><th>Name</th><th>Qty</th><th>HP</th><th>AC</th><th>CR</th>'
            if any(m.get('init') for m in d['monsters']): mons += '<th>Init</th>'
            mons += '<th>Notes</th></tr>'
            for m in m_list:
                mons += f'<tr><td>{esc(m["name"])}</td><td>{m.get("qty",1)}</td><td>{make_dice_html(m.get("hp",""))}</td><td>{esc(m.get("ac",""))}</td><td>{esc(m.get("cr",""))}</td>'
                if any(mm.get('init') for mm in d['monners']): mons += f'<td><b>{esc(m.get("init",""))}</b></td>'
                mons += f'<td>{make_dice_html(m.get("notes",""))}</td></tr>'
            mons += '</table></div>'
        xp_h = ""
        if xp:
            xp_h = f'<div class="wd"><div class="wd-label">Difficulty: <b style="color:{xp["color"]}">{xp["diff"]}</b></div><div class="wd-track"><div class="wd-fill" style="width:{xp["pct"]}%;background:{xp["color"]}"></div></div><div class="wd-xp">Adj. XP: {fmt_n(xp["adj"])} | Easy: {fmt_n(xp["th"]["easy"])} / Med: {fmt_n(xp["th"]["medium"])} / Hard: {fmt_n(xp["th"]["hard"])} / Deadly: {fmt_n(xp["th"]["deadly"])}</div>'
            if xp['suggest']: xp_h += f'<div class="wd-suggest" style="border-color:{xp["color"]}"><b>Tip:</b> {esc(xp["suggest"])}</div>'
            xp_h += '</div>'
        body = f'<div class="wh"><div class="wtl">Encounter</div><h1 class="wtt">{esc(d.get("name","Untitled"))}</h1><div class="wm">{("CR: "+esc(d["cr"]) if d.get("cr") else "") + (" | "+esc(d["environment"]) if d.get("environment") and d.get("cr") else "")}</div></div>{mons}{xp_h}{pv_section("Tactics & Strategy", d.get("tactics"))}{pv_section("Loot Dropped", d.get("loot"))}{pv_section("DM Notes", d.get("notes"))}'
    
    elif wtype == 'loot':
        rows_h = ""
        if d.get('rows') and any(r.get('item') or r.get('range') for r in d['rows']):
            rows_h = f'<div class="ws"><h2 class="wst">Roll on {esc(d.get("rollType","d20"))}</h2><a href="lootroll://" class="dice-btn">🎲 Roll {esc(d.get("rollType","d20"))}</a><span id="dice-result"></span><table class="wt"><tr><th>Roll</th><th>Item</th><th>Qty</th><th>Notes</th></tr>'
            for i, r in enumerate(d['rows']):
                if r.get('item') or r.get('range'):
                    rows_h += f'<tr data-idx="{i}"><td>{esc(r.get("range",""))}</td><td>{make_dice_html(r.get("item",""))}</td><td>{make_dice_html(r.get("qty",""))}</td><td>{esc(r.get("notes",""))}</td></tr>'
            rows_h += '</table></div>'
        body = f'<div class="wh"><div class="wtl">Loot Table</div><h1 class="wtt">{esc(d.get("name","Untitled"))}</h1><div class="wm">Roll: {esc(d.get("rollType","d20"))}</div></div>{rows_h}'
        
    elif wtype == 'spellbook':
        slots_h = ""
        if d.get('spellSlots') and any(s.get('level') for s in d['spellSlots']):
            slots_h = '<div class="ws"><h2 class="wst">Spell Slots</h2>'
            for s in d['spellSlots']:
                if s.get('level'):
                    total, used = int(s.get('total') or 0), int(s.get('used') or 0)
                    dots = "".join(['<div class="slot used"></div>' if i < used else '<div class="slot"></div>' for i in range(total)])
                    slots_h += f'<div class="slot-row"><div class="slot-label">{esc(s["level"])}</div><div class="slots">{dots}</div><div style="font-size:.8rem;color:inherit;opacity:0.7;margin-left:.2rem">{max(0,total-used)}/{total}</div></div>'
            slots_h += '</div>'
        spells_h = ""
        if d.get('spells') and any(s.get('name') for s in d['spells']):
            spells_h = '<div class="ws"><h2 class="wst">Known Spells</h2><table class="wt"><tr><th>Spell</th><th>Level</th><th>School</th><th>Notes</th></tr>'
            for s in d['spells']:
                if s.get('name'): spells_h += f'<tr><td>{esc(s["name"])}</td><td>{esc(s.get("level",""))}</td><td>{esc(s.get("school",""))}</td><td>{make_dice_html(s.get("notes",""))}</td></tr>'
            spells_h += '</table></div>'
        body = f'<div class="wh"><div class="wtl">Spellbook</div><h1 class="wtt">{esc(d.get("name",""))}</h1><div class="wm">{esc(d.get("spellClass",""))}{(" | DC "+esc(d["spellDC"]) if d.get("spellDC") else "")}{(" | Atk "+esc(d["spellAtk"]) if d.get("spellAtk") else "")}</div></div>{slots_h}{spells_h}'

    elif wtype == 'quest':
        objs = ""
        if d.get('objectives') and any(o.get('text') for o in d['objectives']):
            objs = '<div class="ws"><h2 class="wst">Objectives</h2>' + "".join([f'<div class="obj-row"><div class="obj-chk"></div><span>{esc(o["text"])}</span></div>' for o in d['objectives'] if o.get('text')]) + '</div>'
        body = f'<div class="wh"><div class="wtl">Quest</div><h1 class="wtt">{esc(d.get("name","Untitled"))}</h1><div class="wm">{("Given by: "+esc(d["giver"]) if d.get("giver") else "") + (" | "+esc(d["location"]) if d.get("location") else "") + (" | Lv "+esc(d["levelRange"]) if d.get("levelRange") else "")}</div></div>{objs}{pv_section("Rewards", d.get("rewards"))}{pv_section("Complications", d.get("complications"))}{pv_section("Key NPCs", d.get("npcsInvolved"))}{pv_section("Secret Twist", d.get("twist"))}{pv_section("DM Notes", d.get("notes"))}'

    elif wtype == 'faction':
        mems = ""
        if d.get('notableMembers') and any(m.get('name') for m in d['notableMembers']):
            mems = '<div class="ws"><h2 class="wst">Notable Members</h2>' + "".join([f'<div class="mem-card"><div class="mem-name">{esc(m["name"])}</div><div class="mem-role">{esc(m.get("role",""))}{(" — "+esc(m["notes"]) if m.get("notes") else "")}</div></div>' for m in d['notableMembers'] if m.get('name')]) + '</div>'
        body = f'<div class="wh"><div class="wtl">Faction</div><h1 class="wtt">{esc(d.get("name",""))}</h1><div class="wm">{esc(d.get("factionType",""))}{(" | "+esc(d["alignment"]) if d.get("alignment") else "")}</div></div>{pv_section("Resources & Assets", d.get("resources"))}{pv_section("Goals", d.get("goals"))}{pv_section("Methods", d.get("methods"))}{pv_section("Allies", d.get("allies"))}{pv_section("Enemies", d.get("enemies"))}{pv_section("Inner Secrets", d.get("secrets"))}{mems}'

    else: # NPC, Session, Backstory generic handler
        if wtype == 'npc':
            body = f'<div class="wh"><div class="wtl">Non-Player Character</div><h1 class="wtt">{esc(d.get("name","Unnamed"))}</h1><div class="wm">{esc(d.get("raceClass",""))}{(" | "+esc(d["alignment"]) if d.get("alignment") else "")}{(" | Age: "+esc(d["age"]) if d.get("age") else "")}</div></div>{pv_section("Personality Traits", d.get("personalityTraits"))}{pv_section("Ideal", d.get("ideal"))}{pv_section("Bond", d.get("bond"))}{pv_section("Flaw", d.get("flaw"))}{pv_section("Physical Description", d.get("appearance"))}{pv_section("Speaking Mannerisms", d.get("mannerisms"))}{pv_section("Secret", d.get("secret"))}{pv_section("Stat Block Summary", d.get("statBlock"), raw=True)}'
        elif wtype == 'session':
            body = f'<div class="wh"><div class="wtl">Session Notes</div><h1 class="wtt">Session {esc(d.get("number","?"))}</h1><div class="wm">{esc(d.get("date",""))}{(" | "+esc(d["location"]) if d.get("location") else "")}</div></div>{pv_section("Players Present", d.get("players"))}{pv_section("Key Events", d.get("keyEvents"))}{pv_section("NPCs Encountered", d.get("npcsEncountered"))}{pv_section("Combat Encounters", d.get("combats"))}{pv_section("Cliffhanger / Next Hook", d.get("cliffhanger"))}{(f\'<div class="ws"><div class="wfr"><div class="wf"><div class="wfl">XP Awarded</div><div class="wfv">{make_dice_html(d.get("xp",""))}</div></div></div></div>\' if d.get("xp") else "")}{pv_section("Gold & Loot Found", d.get("goldLoot"))}{pv_section("DM Notes", d.get("notes"))}'
        elif wtype == 'backstory':
            body = f'<div class="wh"><div class="wtl">Character Backstory</div><h1 class="wtt">{esc(d.get("name","Unnamed"))}</h1><div class="wm">{esc(d.get("race",""))} {esc(d.get("class",""))}{(" (Lv "+esc(d["level"])+")" if d.get("level") else "")}{(" | "+esc(d["background"]) if d.get("background") else "")}</div></div>{pv_section("Personality Traits", d.get("personalityTraits"))}{pv_section("Ideal", d.get("ideal"))}{pv_section("Bond", d.get("bond"))}{pv_section("Flaw", d.get("flaw"))}{pv_section("Backstory", d.get("backstory"))}{pv_section("Goals & Ambitions", d.get("goals"))}{pv_section("Relationships", d.get("relationships"))}{pv_section("Special Items & Heirlooms", d.get("heirlooms"))}'

    return f"<html><head><style>{css}</style></head><body><div class='wp'>{body}</div></body></html>"


# --- QT CUSTOM WIDGETS ---
class DynListWidget(QWidget):
    dataChanged = None # Will be set by main window
    
    def __init__(self, field_def, parent=None):
        super().__init__(parent)
        self.field_def = field_def
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(2)
        self.rows = []
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ Add Entry")
        add_btn.setStyleSheet("background:rgba(201,149,45,0.15); color:#c9952d; border:1px solid #2e2a23; padding:4px;")
        add_btn.clicked.connect(self.add_row)
        btn_layout.addWidget(add_btn)
        
        if field_def.get('quickAdd'):
            qa_btn = QPushButton("⚡ Quick Add")
            qa_btn.setStyleSheet("background:rgba(201,149,45,0.15); color:#c9952d; border:1px solid #2e2a23; padding:4px;")
            qa_btn.clicked.connect(self.show_quick_add)
            btn_layout.addWidget(qa_btn)
            
        btn_layout.addStretch()
        self.layout.addLayout(btn_layout)

    def add_row(self, data=None):
        row_w = QWidget()
        row_l = QHBoxLayout(row_w)
        row_l.setContentsMargins(0,2,0,2)
        widgets = {}
        for f in self.field_def['fields']:
            if f['t'] == 'number':
                w = QLineEdit(str(data.get(f['k'], f.get('p', ''))) if data else f.get('p', ''))
            else:
                w = QLineEdit(str(data.get(f['k'], '')) if data else '')
            w.setPlaceholderText(f.get('p', ''))
            if f.get('w'): w.setFixedWidth(f['w'])
            if f.get('autocomplete') == 'spell':
                completer = QCompleter([s[0] for s in SPELLS])
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setFilterMode(Qt.MatchContains)
                w.setCompleter(completer)
                w.textChanged.connect(lambda text, widget=w, fd=f: self.autofill_spell(widget, text, row_l))
            row_l.addWidget(w)
            widgets[f['k']] = w
            
        up_btn = QPushButton("▲"); up_btn.setFixedWidth(20); up_btn.clicked.connect(lambda: self.move_row(row_w, -1))
        dn_btn = QPushButton("▼"); dn_btn.setFixedWidth(20); dn_btn.clicked.connect(lambda: self.move_row(row_w, 1))
        rm_btn = QPushButton("✖"); rm_btn.setFixedWidth(20); rm_btn.clicked.connect(lambda: self.remove_row(row_w))
        row_l.addWidget(up_btn); row_l.addWidget(dn_btn); row_l.addWidget(rm_btn)
        
        self.layout.insertWidget(self.layout.count() - 1, row_w)
        self.rows.append((row_w, widgets))
        if self.dataChanged: self.dataChanged()

    def remove_row(self, row_w):
        if len(self.rows) <= 1: return
        idx = next(i for i, (w, _) in enumerate(self.rows) if w == row_w)
        self.layout.removeWidget(row_w)
        row_w.deleteLater()
        self.rows.pop(idx)
        if self.dataChanged: self.dataChanged()

    def move_row(self, row_w, direction):
        idx = next(i for i, (w, _) in enumerate(self.rows) if w == row_w)
        new_idx = idx + direction
        if 0 <= new_idx < len(self.rows):
            self.rows[idx], self.rows[new_idx] = self.rows[new_idx], self.rows[idx]
            self.layout.removeWidget(row_w)
            self.layout.insertWidget(new_idx, row_w)
            if self.dataChanged: self.dataChanged()

    def autofill_spell(self, trigger_widget, text, row_layout):
        if len(text) < 3: return
        for s in SPELLS:
            if s[0].lower() == text.lower():
                inputs = [w for w in row_layout.children() if isinstance(w, QLineEdit)]
                if len(inputs) >= 3 and not inputs[1].text(): inputs[1].setText(s[1])
                if len(inputs) >= 4 and not inputs[2].text(): inputs[2].setText(s[2])
                break

    def show_quick_add(self):
        menu = QMenu(self)
        for m in MONS:
            action = menu.addAction(f"{m[0]} (HP:{m[1]} AC:{m[2]} CR:{m[3]})")
            action.triggered.connect(lambda checked, mon=m: self.add_row({'name':mon[0],'qty':1,'hp':mon[1],'ac':mon[2],'cr':mon[3],'init':'','notes':''}))
        menu.exec_(self.mapToGlobal(self.rect().topLeft()))

    def get_data(self):
        res = []
        for _, widgets in self.rows:
            row_data = {}
            for k, w in widgets.items():
                if w.validator() and isinstance(w.validator(), int): row_data[k] = int(w.text() or 0)
                else: row_data[k] = w.text()
            res.append(row_data)
        return res

    def load_data(self, data_list):
        for w, _ in self.rows: w.deleteLater()
        self.rows.clear()
        for d in data_list: self.add_row(d)


class MainFormWidget(QWidget):
    def __init__(self, app_ref, parent=None):
        super().__init__(parent)
        self.app = app_ref
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10,10,10,10)
        self.widgets = {}
        self.dyn_widgets = {}

    def build_form(self, wtype):
        for w in self.widgets.values(): w.deleteLater()
        for w in self.dyn_widgets.values(): w.deleteLater()
        self.widgets.clear(); self.dyn_widgets.clear()
        
        fields = TYPES[wtype]['fields']
        for f in fields:
            if f.get('type') == 'dyn':
                lbl = QLabel(f['l'])
                lbl.setStyleSheet("font-weight:bold; color:#8a7e6b; font-size:11px; text-transform:uppercase; margin-top:10px;")
                self.layout.addWidget(lbl)
                dyn_w = DynListWidget(f, self)
                dyn_w.dataChanged = self.app.on_data_changed
                self.layout.addWidget(dyn_w)
                self.dyn_widgets[f['k']] = dyn_w
                default_data = self.app.form_data.get(f['k'], [])
                if not default_data: dyn_w.add_row()
                else: dyn_w.load_data(default_data)
            else:
                lbl = QLabel(f['l'])
                lbl.setStyleSheet("font-weight:bold; color:#8a7e6b; font-size:11px; text-transform:uppercase;")
                self.layout.addWidget(lbl)
                
                if f['t'] == 'select':
                    w = QComboBox()
                    w.addItems(f['o'])
                    idx = w.findText(self.app.form_data.get(f['k'], ''))
                    if idx >= 0: w.setCurrentIndex(idx)
                    w.currentTextChanged.connect(lambda text, key=f['k']: self.app.update_field(key, text))
                elif f['t'] == 'textarea':
                    w = QTextEdit()
                    w.setPlainText(self.app.form_data.get(f['k'], ''))
                    w.textChanged.connect(lambda editor=w, key=f['k']: self.app.update_field(key, editor.toPlainText()))
                elif f['t'] == 'number':
                    w = QLineEdit(str(self.app.form_data.get(f['k'], '')))
                    w.textChanged.connect(lambda text, key=f['k']: self.app.update_field(key, int(text) if text.isdigit() else 0))
                else:
                    w = QLineEdit(str(self.app.form_data.get(f['k'], '')))
                    w.textChanged.connect(lambda text, key=f['k']: self.app.update_field(key, text))
                    
                if f.get('w'): w.setFixedWidth(f['w'])
                self.layout.addWidget(w)
                self.widgets[f['k']] = w
        self.layout.addStretch()

    def get_form_data(self):
        data = {k: (w.toPlainText() if isinstance(w, QTextEdit) else (w.currentText() if isinstance(w, QComboBox) else w.text())) for k, w in self.widgets.items()}
        for k, dw in self.dyn_widgets.items(): data[k] = dw.get_data()
        return data


# --- MAIN WINDOW ---
class DNDWorksheetForge(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&D Worksheet Forge")
        self.resize(1200, 800)
        
        self.defaults = get_defaults()
        self.saved_data = []
        self.current_type = 'encounter'
        self.form_data = json.loads(json.dumps(self.defaults['encounter']))
        self.editing_id = None
        self.dark_preview = False
        self.data_path = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) / "dnd_ws_save.json"
        self.undo_stack = QUndoStack(self)
        self.auto_save_timer = QTimer()
        self.auto_save_timer.setSingleShot(True)
        self.auto_save_timer.timeout.connect(self.do_auto_save)
        
        self.load_from_disk()
        self.init_ui()
        self.apply_theme(False)
        self.refresh_all()

    def init_ui(self):
        # Toolbar
        tb = QToolBar("Main Toolbar")
        tb.setMovable(False)
        self.addToolBar(tb)
        
        tb.addAction("💾 Save", self.save_ws)
        tb.addAction("📄 New", self.new_ws)
        tb.addAction("📋 Duplicate", self.dup_ws)
        tb.addAction("🗑️ Delete", self.del_ws)
        tb.addSeparator()
        tb.addAction("↩️ Undo", self.undo_stack.undo)
        tb.addAction("↪️ Redo", self.undo_stack.redo)
        tb.addSeparator()
        tb.addAction("🖨️ Print", self.print_ws)
        tb.addAction("📥 Import", self.import_data)
        tb.addAction("📤 Export", self.export_data)
        tb.addSeparator()
        self.theme_action = tb.addAction("🌙 Dark Preview", self.toggle_preview_theme)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar_l = QVBoxLayout(sidebar)
        sidebar_l.setContentsMargins(5,5,5,5)
        
        self.type_list = QListWidget()
        for k, v in TYPES.items():
            item = QListWidgetItem(f"{v['icon']} {v['label']}")
            item.setData(Qt.UserRole, k)
            self.type_list.addItem(item)
        self.type_list.currentRowChanged.connect(self.switch_type)
        self.type_list.setCurrentRow(0)
        sidebar_l.addWidget(QLabel("<b>Worksheet Types</b>"))
        sidebar_l.addWidget(self.type_list)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search saved...")
        self.search_bar.textChanged.connect(self.refresh_saved_list)
        sidebar_l.addWidget(self.search_bar)
        
        self.saved_list = QListWidget()
        self.saved_list.itemDoubleClicked.connect(self.load_ws)
        sidebar_l.addWidget(self.saved_list)
        
        # Main Area
        splitter = QSplitter(Qt.Horizontal)
        
        scroll_form = QScrollArea()
        self.form_widget = MainFormWidget(self)
        scroll_form.setWidget(self.form_widget)
        scroll_form.setWidgetResizable(True)
        
        self.preview = QTextBrowser()
        self.preview.setOpenExternalLinks(False)
        self.preview.anchorClicked.connect(self.handle_preview_click)
        
        splitter.addWidget(sidebar)
        splitter.addWidget(scroll_form)
        splitter.addWidget(self.preview)
        splitter.setSizes([220, 500, 480])
        self.setCentralWidget(splitter)
        
        self.statusBar().showMessage("Ready")

    def apply_theme(self, dark):
        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #1a1815; color: #e8dcc8; font-family: 'Segoe UI', sans-serif; }
            QToolBar { background: #242119; border-bottom: 1px solid #2e2a23; spacing: 5px; padding: 3px; }
            QToolBar QToolButton { background: #242119; color: #e8dcc8; border: 1px solid #2e2a23; padding: 4px 8px; border-radius: 3px; font-size: 12px; }
            QToolBar QToolButton:hover { background: #c9952d; color: #1a1200; }
            QLineEdit, QTextEdit, QComboBox { background: #242119; color: #e8dcc8; border: 1px solid #2e2a23; border-radius: 3px; padding: 4px; }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 1px solid #c9952d; }
            QComboBox::drop-down { border: none; } QComboBox QAbstractItemView { background: #242119; color: #e8dcc8; selection-background-color: #c9952d; }
            QListWidget { background: #1a1815; color: #e8dcc8; border: 1px solid #2e2a23; border-radius: 3px; }
            QListWidget::item { padding: 4px; border-bottom: 1px solid #2e2a23; } QListWidget::item:selected { background: rgba(201,149,45,0.2); color: #c9952d; }
            QTextBrowser { background: #12100d; border: none; }
            QScrollBar:vertical { background: #1a1815; width: 8px; } QScrollBar::handle:vertical { background: #2e2a23; border-radius: 4px; min-height: 20px; }
            QStatusBar { background: #151210; color: #8a7e6b; }
        """)

    def switch_type(self, idx):
        if idx < 0: return
        wtype = self.type_list.item(idx).data(Qt.UserRole)
        if self.current_type == wtype: return
        self.current_type = wtype
        self.form_data = json.loads(json.dumps(self.defaults[wtype]))
        self.editing_id = None
        self.undo_stack.clear()
        self.refresh_all()

    def update_field(self, key, value):
        # Simple update bypassing heavy undo for typing, rely on auto-save
        self.form_data[key] = value
        self.update_preview()
        self.trigger_auto_save()

    def on_data_changed(self):
        # Called by DynListWidget
        for k, dw in self.form_widget.dyn_widgets.items():
            self.form_data[k] = dw.get_data()
        self.update_preview()
        self.trigger_auto_save()

    def trigger_auto_save(self):
        self.auto_save_timer.start(2000)
        self.statusBar().showMessage("Unsaved changes...")

    def do_auto_save(self):
        if not self.editing_id: return
        self.save_to_disk()
        self.statusBar().showMessage("Auto-saved", 2000)

    def update_preview(self):
        # Gather latest data including dyn lists
        for k, dw in self.form_widget.dyn_widgets.items():
            self.form_data[k] = dw.get_data()
        html = gen_html(self.form_data, self.current_type, self.dark_preview)
        self.preview.setHtml(html)

    def refresh_all(self):
        self.form_widget.build_form(self.current_type)
        self.update_preview()
        self.refresh_saved_list()

    def refresh_saved_list(self):
        self.saved_list.clear()
        search = self.search_bar.text().lower()
        for ws in self.saved_data:
            name = ws['data'].get('name', 'Untitled')
            if search and search not in name.lower() and search not in ws['type'].lower(): continue
            color = TYPE_COLORS.get(ws['type'], '#888')
            item = QListWidgetItem(f"● {name} ({TYPES[ws['type']]['label']})")
            item.setData(Qt.UserRole, ws['id'])
            item.setForeground(QColor(color))
            if ws['id'] == self.editing_id: item.setBackground(QColor(40,35,28))
            self.saved_list.addItem(item)

    def save_ws(self):
        for k, dw in self.form_widget.dyn_widgets.items():
            self.form_data[k] = dw.get_data()
            
        if self.editing_id:
            for ws in self.saved_data:
                if ws['id'] == self.editing_id:
                    ws['data'] = json.loads(json.dumps(self.form_data))
                    break
        else:
            self.editing_id = f"{random.randint(1000,9999)}"
            self.saved_data.append({'id': self.editing_id, 'type': self.current_type, 'data': json.loads(json.dumps(self.form_data))})
        
        self.save_to_disk()
        self.refresh_saved_list()
        self.statusBar().showMessage("Saved successfully", 2000)

    def load_ws(self, item):
        ws_id = item.data(Qt.UserRole)
        for ws in self.saved_data:
            if ws['id'] == ws_id:
                self.current_type = ws['type']
                self.form_data = json.loads(json.dumps(ws['data']))
                self.editing_id = ws['id']
                self.undo_stack.clear()
                
                # Update type list selection
                for i in range(self.type_list.count()):
                    if self.type_list.item(i).data(Qt.UserRole) == self.current_type:
                        self.type_list.blockSignals(True)
                        self.type_list.setCurrentRow(i)
                        self.type_list.blockSignals(False)
                        break
                self.refresh_all()
                self.statusBar().showMessage("Loaded worksheet", 2000)
                break

    def new_ws(self):
        self.form_data = json.loads(json.dumps(self.defaults[self.current_type]))
        self.editing_id = None
        self.undo_stack.clear()
        self.refresh_all()

    def dup_ws(self):
        if not self.editing_id: return
        new_data = json.loads(json.dumps(self.form_data))
        new_data['name'] = new_data.get('name', 'Worksheet') + " (Copy)"
        new_id = f"{random.randint(1000,9999)}"
        self.saved_data.append({'id': new_id, 'type': self.current_type, 'data': new_data})
        self.save_to_disk()
        self.refresh_saved_list()
        self.statusBar().showMessage("Duplicated", 2000)

    def del_ws(self):
        if not self.editing_id: return
        self.saved_data = [ws for ws in self.saved_data if ws['id'] != self.editing_id]
        self.editing_id = None
        self.new_ws()
        self.save_to_disk()

    def print_ws(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.NativeFormat)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.Accepted:
            self.preview.print(printer)

    def toggle_preview_theme(self):
        self.dark_preview = not self.dark_preview
        self.theme_action.setText("☀️ Light Preview" if self.dark_preview else "🌙 Dark Preview")
        self.update_preview()

    def handle_preview_click(self, url):
        url_str = url.toString()
        if url_str.startswith("dice://"):
            parts = url_str.replace("dice://", "").split('/')
            if len(parts) == 3:
                n, s, mod = int(parts[0]), int(parts[1]), int(parts[2])
                rolls = [random.randint(1, s) for _ in range(n)]
                total = sum(rolls) + mod
                self.statusBar().showMessage(f"Rolled {n}d{s}{mod if mod!=0 else ''}: {rolls} = {total}", 4000)
        elif url_str.startswith("lootroll://"):
            d = self.form_data
            sides = int(d.get('rollType', 'd20').replace('d',''))
            roll = random.randint(1, sides)
            rows = d.get('rows', [])
            match_idx = -1
            for i, r in enumerate(rows):
                rng = r.get('range', '')
                if '-' in rng:
                    a, b = map(int, rng.split('-'))
                    if a <= roll <= b: match_idx = i; break
                elif rng.isdigit() and int(rng) == roll: match_idx = i; break
            
            self.statusBar().showMessage(f"Rolled {sides}: {roll} -> {'Hit!' if match_idx>=0 else 'Miss'}", 4000)
            # Highlight row via simple JS injection alternative (manipulate HTML directly)
            current_html = self.preview.toHtml()
            if match_idx >= 0:
                # Very basic string replace to add highlight class for visual feedback
                clean_html = current_html.replace(f'data-idx="{match_idx}"', f'data-idx="{match_idx}" class="row-hl"')
                self.preview.setHtml(clean_html)
                QTimer.singleShot(1500, self.update_preview) # Reset after 1.5s

    def import_data(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Worksheets", "", "JSON Files (*.json)")
        if path:
            with open(path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.saved_data.extend(data)
                    self.save_to_disk()
                    self.refresh_saved_list()
                    self.statusBar().showMessage(f"Imported {len(data)} worksheets", 2000)

    def export_data(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Worksheets", "dnd_worksheets.json", "JSON Files (*.json)")
        if path:
            with open(path, 'w') as f:
                json.dump(self.saved_data, f, indent=2)
            self.statusBar().showMessage("Exported successfully", 2000)

    def save_to_disk(self):
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, 'w') as f:
            json.dump(self.saved_data, f, indent=2)

    def load_from_disk(self):
        if self.data_path.exists():
            try:
                with open(self.data_path, 'r') as f:
                    self.saved_data = json.load(f)
            except: self.saved_data = []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = DNDWorksheetForge()
    window.show()
    sys.exit(app.exec())