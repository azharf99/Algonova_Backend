levels = {
    "Artificial Intelligence, AI ENG" : "Artificial Intelligence",
    "Visual programming INDONESIA" : "IT GENIUS level 3",
    "Frontend Development_ENG" : "Frontend Development",
    "Python Start 1st year IND" : "IT HERO level 6",
    "Python Start 1st year ENG" : "IT HERO level 6",
    "Python Start 2d year IND" : "IT HERO level 7",
    "Python Start 2d year ENG" : "IT HERO level 7",
    "Python Pro 1st year 2021-2022 ind" : "IT HERO level 8",
    "Python Pro_1_ENG" : "IT HERO level 8",
    "Python Pro 2 IND" : "IT HERO level 9",
    "Python Pro 2 ENG" : "IT HERO level 9",
}


def get_course_level(modul):
    return levels.get(modul)