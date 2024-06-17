from _resources.models import Resource

RESOURCES = {
    "fabula-podr" : Resource("Podręcznik Fabula Ultima","./resources/fabulapodr.pdf",True),
    "fate-podr" : Resource("Podręcznik Fate Core","./resources/fatepodr.pdf", True),
    "cyberpunk-podr" : Resource("Podręcznik Cyberpunk Red","./resources/cyberprankpodr.pdf",True),
    "fabula-kp" : Resource("Karta Postaci do Fabula Ultima","./resources/fabulakp.pdf", True),
    "fate-kp" : Resource("Karta postaci do Fate Core","./resources/fatekp.pdf", True),
    "cyberpunk-kp" : Resource("Karta postaci do Cyberpuk Red", "./resources/cyberprankkp.pdf", True),
    "fate-skills" : Resource("Umiejętności Fate Core", "./resources/umiejki.png", True),
    "fate-stunts" : Resource("Sztuczki Fate Core", "http://evilhat.wikidot.com/fate-core-stunts", False)
}