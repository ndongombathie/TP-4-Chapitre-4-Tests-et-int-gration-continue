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

Le `Jenkinsfile` couvre **CI + une partie du Continuous Delivery (la
qualité)**, mais pas la release. On retrouve :
- **CI** : code source (`Récupération du code`, checkout scm) + build
  (`Build` : `manage.py check` et `collectstatic --dry-run`) + tests
  (`Tests` : `manage.py test`).
- **Qualité (étape en plus de la CI)** : `Standard de code (lint)`
  (flake8) et les deux stages sécurité `Sécurité - SAST` (semgrep) et
  `Sécurité - SCA` (pip-audit).
- En revanche, **aucune étape de release** (de production) n'existe : le
  pipeline s'arrête après la validation, il ne fabrique ni ne publie
  d'artefact livrable.

**Ce qui manquerait pour aller plus loin :**

Pour atteindre le **Continuous Delivery complet**, il faudrait ajouter un
stage de **release manuelle** : un stage `Release` avec la directive
`input` (validation humaine dans Jenkins, « approuver ? ») qui construise
un artefact réutilisable (wheel/sdist Python via `python -m build`, ou une
image Docker poussée vers le registry) puis le publie (ex. `__release__` /
GitHub release, PyPI privé…).

Pour atteindre le **déploiement continu**, la validation « input » est
remplacée par le même stage de release **automatisé**, suivi d'un stage de
**déploiement** (`Deploy`) qui publie vers l'environnement de production
(serveur, PaaS, Kubernetes…) avec, si besoin, une vérification post-
déploiement (sonde/healthcheck). Tout devient automatique : commit →
tests → qualité → build → déploiement en production sans intervention
humaine.

## 5. Tests non fonctionnels hors scope

Le chapitre 4 liste aussi les tests capacitaires et de compatibilité,
absents de ce pipeline. Pourquoi, à l'échelle de ce TP, est-ce un choix
raisonnable plutôt qu'un oubli (indice : YAGNI, chapitre 2) ? Que
faudrait-il ajouter si SunuSanté grandissait réellement ?

C'est un choix raisonnable car c'est un TP : l'application balance des
fichiers entre deux dossiers sur une machine de développement. Aucune
**contrainte de charge** (nombre d'utilisateurs, volume de fichiers) ni de
**matrice de compatibilité** (OS/navigateurs) n'est exigée par le sujet.
Ces tests coûteraient du temps de configuration et de maintenance (serveurs
de charge, parcs de navigateurs) pour zéro exigence derrière — c'est
exactement le **YAGNI** vu au chapitre 2 : on n'ajoute pas une capacité dont
on n'a pas prouvé le besoin. Les exclure n'est pas un oubli mais un
périmètre assumé.

Si SunuSanté grandissait réellement, on ajouterait :
- **Tests capacitaires (charge/performance)** : par ex. **JMeter** ou
  **Locust** pour simuler des utilisateurs/fichiers concurrents, avec des
  seuils de débit et de temps de réponse à vérifier dans le pipeline (un
  stage `Tests de charge` qui échoue au-delà du seuil).
- **Tests de compatibilité** : **Matrix/multi-versions** (tester sous
  plusieurs versions Python/OS — déjà facilité par l'agent Docker), et pour
  une appli web, **Selenium** ou **Playwright** sur plusieurs navigateurs.
- Typiquement, **les tests non fonctionnels passent plus tard dans le
  cycle** (après les tests fonctionnels, voire au moment de la release),
  car ils sont plus lents et plus coûteux à exécuter.
- Une fois ces exigences réellement apparues (gros volume, support multi-
  plateforme), le YAGNI céderait la place à un besoin prouvé, et ces stages
  s'intégreraient naturellement au pipeline.
