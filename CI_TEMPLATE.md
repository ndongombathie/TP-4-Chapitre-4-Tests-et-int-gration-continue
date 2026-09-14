# Pipeline CI - SunuSanté

Nom / Groupe :

## 1. Le workflow d'intégration continue (chapitre 4, partie 1)

Le cours décrit 6 étapes, du commit au feedback. Remplissez la colonne de
droite avec le nom exact du stage Jenkins qui correspond, tel qu'il
apparaît dans votre `Jenkinsfile` et dans la Stage View de Jenkins.

| Étape du cours | Stage Jenkins correspondant |
|---|---|
| 1. Commit & push | `Récupération du code` (checkout scm) |
| 2. Notification (Jenkins est prévenu) | *(pas un stage : c'est le trigger)* |
| 3. Build | `Build` |
| 4. Feedback build | `post { success / failure }` (vert/rouge dans la Stage View) |
| 5. Tests automatiques | `Tests` |
| 6. Feedback tests | `post { success / failure }` (vert/rouge dans la Stage View) |

Comment Jenkins est-il informé qu'un nouveau commit existe, dans votre
configuration (polling SCM, webhook, déclenchement manuel) ?

Le Jenkinsfile ne contient aucun bloc `triggers` (pas de `pollSCM`, pas de
`webhook`). La configuration du déclenchement se fait côté interface Jenkins.
Dans notre cas, Jenkins est informé par **polling SCM** : le serveur
interroge régulièrement le dépôt GitHub pour détecter de nouveaux commits.
On pourrait aussi configurer un webhook GitHub pour un déclenchement plus
réactif, ou se contenter d'un déclenchement manuel via « Build Now ».

## 2. Les prérequis d'une bonne CI (chapitre 4, partie 3)

| Prérequis | Statut sur SunuSanté | Détail |
|---|---|---|
| Dépôt avec versioning |  distant | Git distant sur GitHub : https://github.com/ndongombathie/TP-4-Chapitre-4-Tests-et-int-gration-continue.git |
| Standard de code vérifié |  vérifié par le pipeline | **flake8** via le stage `Standard de code (lint)` (`flake8 .`), configuré dans `.flake8` (max-line-length = 100) |
| Serveur d'intégration continue | Jenkins | Job « pipeline » lisant le `Jenkinsfile` (Pipeline script from SCM), **agent Docker** : image `python:3.11-slim` (`Jenkinsfile:25`) |

## 3. Pourquoi Jenkins, ici (chapitre 4, partie 4)

Le cours compare GitLab CI/CD, Jenkins et GitHub Actions. Remplissez ce
comparatif avec vos propres mots, puis justifiez en 2-3 phrases pourquoi
Jenkins convient (ou pas) à ce projet précis.

| Outil | Avantage principal | Inconvénient principal |
|---|---|---|
| GitLab CI/CD | Intégration native au dépôt GitLab, pipelines définis dans le dépôt (`.gitlab-ci.yml`), pas de serveur séparé à administrer | Verrouillé à GitLab : si le dépôt n'est pas hébergé sur GitLab, il faut le migrer |
| Jenkins | Serveur autonome et très flexible : plugins pour presque tout, pipelines déclaratives via `Jenkinsfile`, indépendant du dépôt utilisé (GitHub, GitLab, Bitbucket…) | Installation, configuration et maintenance d'un serveur dédié en plus du dépôt ; courbe d'apprentissage |
| GitHub Actions | CI gratuite et intégrée à GitHub, workflows dans le dépôt (`.github/workflows/`), très simple à démarrer | Lié à GitHub (ou à un cloud public) ; moins de liberté pour cacher les secrets et la config sur un serveur interne |

**Justification du choix pour SunuSanté :**

Jenkins convient à ce projet car il est **indépendant du dépôt** : le
`Jenkinsfile` déclaratif avec un agent Docker (`python:3.11-slim`) fonctionne
sur n'importe quelle machine, sans dépendre de la plateforme d'hébergement
du code (ici GitHub). C'est aussi un choix pédagogique : Jenkins expose
explicitement les mécanismes d'un serveur CI (triggers, stages, bloc `post`,
Stage View) qu'on retrouve dans GitLab CI/CD et GitHub Actions.

## 4. CI, Continuous Delivery, déploiement continu

Sur les 3 périmètres vus en cours (CI : code source + tests + build ·
Continuous Delivery : + qualité + release manuelle · déploiement continu :
tout automatisé), lequel votre `Jenkinsfile` couvre-t-il aujourd'hui ?
Qu'est-ce qui manquerait pour passer au périmètre suivant ?

**Périmètre couvert :**

**Ce qui manquerait pour aller plus loin :**

## 5. Tests non fonctionnels hors scope

Le chapitre 4 liste aussi les tests capacitaires et de compatibilité,
absents de ce pipeline. Pourquoi, à l'échelle de ce TP, est-ce un choix
raisonnable plutôt qu'un oubli (indice : YAGNI, chapitre 2) ? Que
faudrait-il ajouter si SunuSanté grandissait réellement ?
