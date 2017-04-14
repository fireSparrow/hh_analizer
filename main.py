
from parser import VacanciesListParser, VacancyParser

import analyzer
import visualizer


vlp = VacanciesListParser()
vlp.run()

vacancies = []
for id_ in vlp:
    vp = VacancyParser(id_)
    vp.run()
    vacancies.append(vp)

"""
all_key_skills = [v.key_skills for v in vacancies
                  if v.key_skills]

data = analyzer.calc_2d_projection(all_key_skills)
visualizer.plot_2d_projection(data)
"""

all_requirements = [v.requirements for v in vacancies]
print(all_requirements)