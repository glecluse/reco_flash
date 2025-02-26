import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

st.title("Évaluation de la compétitivité de votre entreprise")

# Initialisation des réponses et de la progression
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "step" not in st.session_state:
    st.session_state.step = 0

questions = [
    ("Vision à Long Terme", "Quelle est votre vision à long terme ?", [ #q1
        "J'ai une idée précise de la mission de mon entreprise et de sa vision.",
        "Ma mission est claire, mais je n'ai pas encore défini ma vision à long terme.",
        "Je comprends l'importance de la vision mais je ne l'ai pas encore définie.",
        "Je ne vois pas l'intérêt d'avoir une vision à long terme pour mon entreprise."
    ]),
    ("Tendances du Secteur", "Comment suivez-vous les tendances de votre secteur ?", [ #q2
        "J'ai une compréhension claire des tendances actuelles dans mon secteur.",
        "Je connais certaines tendances dans mon secteur, mais je ne suis pas sûr de leur impact.",
        "J'essaie de suivre les tendances, mais je n'ai pas une vision claire.",
        "Je n'ai pas pris le temps d'analyser les tendances de mon secteur."
    ]),
    ("Proposition de Valeur Unique", "Comment évaluez-vous la clarté et la différenciation de votre proposition de valeur ?", [ #q3
        "Ma proposition de valeur est claire et me différencie bien de la concurrence.",
        "J'ai une proposition de valeur, mais elle pourrait être affinée pour mieux me différencier.",
        "Je sais que j'ai besoin d'une proposition de valeur, mais je ne l'ai pas encore définie.",
        "Je ne vois pas ce que c'est qu'une proposition de valeur."
    ]),
    ("Le Bon Prix","Quelle est votre situation actuelle en matière de tarification et comment cela affecte-t-il la satisfaction de vos clients et la rentabilité de votre entreprise ?", [ #q4
        "J’ai une grille tarifaire claire, permettant une marge confortable.",
        "Ma grille tarifaire existe, mais ne marge pas assez.",
        "J’ai une grille tarifaire, mais elle est complexe et pas toujours cohérente.",
        "Je n’ai pas de grille tarifaire clairement définie."
    ]),
    ("Suivi des Marges par Produit/Service","Comment suivez-vous actuellement la rentabilité de vos produits ou services, et quels outils utilisez-vous pour optimiser vos marges ?", [ #q5
        "J’ai une vision claire de la rentabilité de chaque produit/service. Je suis en mesure d’ajuster les prix ou les coûts en fonction des marges.",
        "Je connais globalement les marges, mais il me manque des outils pour un suivi précis et régulier.",
        "Je ne suis pas vraiment certain des marges de chaque produit/service. Je n’ai pas de système en place pour suivre les rentabilités de manière détaillée.",
    ]),
    ("Comment pouvez-vous attirer l'attention de vos prospects ?","Qui sont vos clients cibles ?", [ #q6
        "J'ai des actions marketing efficaces pour attirer mes prospects et je les analyse régulièrement.",
        "Je mets en place des actions marketing, mais je n’évalue pas toujours leur efficacité.",
        "J’ai quelques actions marketing, mais elles sont dispersées et peu structurées.",
        "Je ne mets pas en place de stratégie pour attirer mes prospects.",
    ]),
    ("Qu'est-ce qui rendra votre service ou produit exceptionnel ?","Qu'est-ce qui rendra votre service ou produit exceptionnel ?", [ #q7
        "Je sais exactement ce qui rend mon produit ou service unique et je le mets en avant.",
        "J'ai quelques éléments différenciateurs, mais je pourrais les exploiter davantage.",
        "Je n’ai pas encore identifié ce qui rend mon produit/service exceptionnel.",
        "Je ne vois pas l'importance de différencier mon produit/service.",
    ]),
    ("Comment allez-vous fidéliser vos clients ?","Comment allez-vous fidéliser vos clients ?", [ #q8
    "J'ai mis en place des actions concrètes et régulières pour fidéliser mes clients.",
    "Je suis en train de développer des actions pour fidéliser mes clients, mais elles ne sont pas encore structurées.",
    "J'ai des clients fidèles, mais je n'ai pas de programme dédié pour les fidéliser.",
    "Je ne mets pas l'accent sur la fidélisation de mes clients.",
    ]),
    ("Utilisez-vous un CRM pour suivre vos prospects et clients ?","Utilisez-vous un CRM pour suivre vos prospects et clients ?", [ #q9
        "J’utilise un CRM efficace pour suivre mes prospects et clients.",
        "J’utilise un CRM, mais je ne l’exploite pas pleinement.",
        "Je sais qu’un CRM pourrait m’aider, mais je ne l’ai pas encore mis en place.",
        "Je ne vois pas l’intérêt d’utiliser un CRM.",
    ]),
    ("Compétences et Recrutement","Votre équipe possède-t-elle les compétences nécessaires pour assurer une performance optimale ?", [ #q10
        "L’équipe possède toutes les compétences nécessaires et chaque membre est parfaitement adapté à son rôle.",
        "L’équipe est compétente, mais quelques domaines clés nécessitent des améliorations.",
        "L’équipe manque de compétences dans certains domaines spécifiques, ce qui crée des obstacles.",
        "Il y a un manque important de compétences clés dans l’équipe, affectant la performance globale.",
    ]),
    ("Avez-vous des KPIs définis pour suivre votre performance commerciale (CA, taux de conversion, panier moyen) ?","Avez-vous des KPIs définis pour suivre votre performance commerciale (CA, taux de conversion, panier moyen) ?", [ #q11
        "J’ai des KPIs clairs et je les suis régulièrement pour ajuster ma stratégie.",
        "J’ai quelques KPIs définis, mais je ne les analyse pas systématiquement.",
        "Je n’ai pas encore de KPIs précis pour mesurer ma performance.",
        "Je ne vois pas l’utilité de suivre des KPIs.",
    ]),
    ("Organisation et Structure","Comment évaluez-vous l'organisation et la structure interne de votre entreprise ?", [ #q12
        "L'organisation interne de l'entreprise est claire et bien structurée, facilitant la communication entre collègues et dirigeants et la prise de décision.",
        "L'organisation est en place, mais manque de certaines clarifications ou alignements au sein des équipes.",
        "Il y a des ambiguïtés dans l'organisation, créant des zones de confusion.",
        "L'organisation est chaotique, entraînant des décisions mal informées et une communication inefficace.",
    ]),
    ("Compétences et Recrutement","Comment évaluez-vous les compétences dans votre entreprise ?", [ #q13
        "L’équipe possède toutes les compétences nécessaires et chaque membre est parfaitement adapté à son rôle.",
        "L’équipe est compétente, mais quelques domaines clés nécessitent des améliorations.",
        "L’équipe manque de compétences dans certains domaines spécifiques, ce qui crée des obstacles.",
        "Il y a un manque important de compétences clés dans l’équipe, affectant la performance globale.",
    ]),
    ("Optimisation des processus","Dans quelle mesure vos processus sont-ils optimisés et automatisés pour maximiser l’efficacité ?", [ #q14
        "Tous les processus sont optimisés et automatisés pour améliorer l’efficacité.",
        "Les processus sont relativement optimisés, mais certains aspects peuvent encore être améliorés.",
        "De nombreux processus sont inefficaces et ralentissent les opérations.",
        "Il y a un grand nombre de processus obsolètes ou mal gérés, provoquant des retards et des erreurs.",
    ]),
    ("Motivation et productivité","Quel est le niveau de motivation et de productivité de votre équipe ?", [ #q15
        "Il n'y a pas de personnes irremplaçables, car nous avons une bonne répartition des compétences et des connaissances.",
        "Nous avons identifié des personnes clés, mais nous travaillons à réduire cette dépendance.",
        "Il y a quelques personnes clés, mais nous avons des plans de contingence en place.",
        "Oui, certaines personnes sont cruciales et leur départ pourrait impacter fortement l’entreprise.",
    ]),
    ("Gestion des savoirs","Comment la gestion des savoirs est-elle organisée au sein de votre entreprise ?", [ #q16
        "Un système de gestion des savoirs est en place, permettant de partager facilement les connaissances au sein de l’entreprise.",
        "Il existe un début de gestion des savoirs, mais certains éléments importants sont encore dispersés.",
        "Il y a une perte de savoirs clés au sein de l’équipe, avec un manque de partage d’informations.",
        "Il n'y a pas de gestion des savoirs, ce qui conduit à la perte d'expertise et à l’inefficacité.",
    ]),
    ("Rôles et responsabilités","Les rôles et responsabilités de chaque membre de l’équipe sont-ils clairement définis et compris ?", [ #q17
        "Les rôles et responsabilités de chaque membre de l’équipe sont parfaitement définis et bien compris.",
        "Les rôles sont définis, mais il y a quelques ambiguïtés sur certaines responsabilités.",
        "Certains rôles sont flous, ce qui entraîne des zones de confusion au sein de l’équipe.",
        "Il n'y a aucune clarté sur les rôles et responsabilités, ce qui mène à des conflits et erreurs internes.",
    ]),
    ("Suivi de la rentabilité","Le suivi de la rentabilité est-il réalisé de manière régulière et avec des données complètes ?", [ #q18
        "La rentabilité est suivie de manière régulière grâce à un tableau de bord financier clair.",
        "Un suivi est en place, mais il manque certaines informations pour une évaluation complète de la rentabilité.",
        "La rentabilité est parfois suivie, mais de manière désorganisée et peu fiable.",
        "Il n’y a pas de suivi systématique de la rentabilité, ce qui entraîne des erreurs dans la gestion financière.",
    ]),
    ("Gestion de la trésorerie","La gestion de la trésorerie est-elle optimisée avec des prévisions régulières et une bonne visibilité des flux financiers ?", [ #q19
        "La trésorerie est gérée efficacement avec des prévisions claires et une bonne visibilité.",
        "Un plan de trésorerie est en place, mais les prévisions ne sont pas toujours révisées régulièrement.",
        "La gestion de la trésorerie est partiellement optimisée, mais certaines informations cruciales manquent.",
        "La trésorerie est mal gérée, avec des imprévus fréquents affectant la liquidité de l’entreprise.",
    ]),
    ("Identification des risques financiers","Les risques financiers de l'entreprise sont-ils clairement identifiés et gérés avec des stratégies de couverture appropriées ?", [ #q20
        "Les risques financiers sont clairement identifiés et des stratégies de prévention sont en place.",
        "Certains risques sont identifiés, mais des stratégies de couverture sont encore à mettre en place.",
        "Les risques financiers sont partiellement identifiés, mais aucun plan de gestion n’est instauré.",
        "Les risques financiers ne sont pas identifiés ni gérés, créant une vulnérabilité à des pertes majeures.",
    ]),
    ("Plan de financement","Votre entreprise dispose-t-elle d’un plan de financement clair et adapté pour soutenir sa croissance et faire face aux imprévus ?", [ #q21
        "Un plan de financement solide est en place pour soutenir la croissance de l’entreprise.",
        "Le plan de financement existe, mais il manque de flexibilité pour faire face à des imprévus.",
        "Un plan de financement partiel est en place, mais il ne couvre pas tous les besoins de l’entreprise.",
        "L’entreprise n’a pas de plan de financement clairement défini, ce qui limite les possibilités de croissance.",
    ]),
    ("Indicateurs financiers de rentabilité","Disposez-vous d’un tableau de bord financier complet et à jour pour suivre les indicateurs de rentabilité de votre entreprise ?", [ #q22
        "Le tableau de bord financier inclut des indicateurs clairs tels que la marge brute, la marge nette, et les ratios de rentabilité.",
        "Les indicateurs financiers sont suivis de manière partielle, mais manquent d’informations essentielles pour une analyse complète.",
        "Il existe quelques indicateurs financiers, mais ils ne sont pas utilisés de manière cohérente.",
        "Aucun tableau de bord financier n’est mis en place pour suivre les indicateurs clés de rentabilité, ce qui entraîne des décisions mal informées.",
    ]),
    ("Suivi des créances","Comment évaluez-vous votre suivi des créances clients et la gestion des délais de paiement ?", [ #q23
    "Un suivi rigoureux des créances clients est mis en place avec un contrôle des délais de paiement.",
    "Le suivi des créances est partiellement en place, mais il manque de rigueur pour éviter les impayés.",
    "Il existe un suivi sporadique des créances, mais les délais sont souvent ignorés.",
    "Aucune gestion régulière des créances clients, entraînant des problèmes de liquidité.",
    ]),    
    ]

# Affichage progressif des questions
if st.session_state.step < len(questions):
    category, question, options = questions[st.session_state.step]

    st.markdown(f"### {question}")
    response = st.radio("", options, key=f"q{st.session_state.step}")

    if st.button("Suivant"):
        st.session_state.responses[category] = response
        st.session_state.step += 1
        st.rerun()  # Correction ici

# Affichage du rapport final
#elif st.session_state.step == len(questions):
#    st.success("Merci d'avoir complété l'évaluation ! Voici votre rapport :")
#    for category, answer in st.session_state.responses.items():
#        st.write(f"**{category}** : {answer}")

    #a_question_category = questions[0][0]  # Récupère la catégorie de la première question

if st.session_state.step == len(questions):

    st.title("Compte-rendu de vos réponses")

    reponse1 = st.session_state.responses.get(questions[0][0], 'Non répondu')
    reponse2 = st.session_state.responses.get(questions[1][0], 'Non répondu')
    reponse3 = st.session_state.responses.get(questions[2][0], 'Non répondu')
    reponse4 = st.session_state.responses.get(questions[3][0], 'Non répondu')
    reponse5 = st.session_state.responses.get(questions[4][0], 'Non répondu')
    reponse6 = st.session_state.responses.get(questions[5][0], 'Non répondu')
    reponse7 = st.session_state.responses.get(questions[6][0], 'Non répondu')
    reponse8 = st.session_state.responses.get(questions[7][0], 'Non répondu')
    reponse9 = st.session_state.responses.get(questions[8][0], 'Non répondu')
    reponse10 = st.session_state.responses.get(questions[9][0], 'Non répondu')
    reponse11 = st.session_state.responses.get(questions[10][0], 'Non répondu')
    reponse12 = st.session_state.responses.get(questions[11][0], 'Non répondu')
    reponse13 = st.session_state.responses.get(questions[12][0], 'Non répondu')
    reponse14 = st.session_state.responses.get(questions[13][0], 'Non répondu')
    reponse15 = st.session_state.responses.get(questions[14][0], 'Non répondu')
    reponse16 = st.session_state.responses.get(questions[15][0], 'Non répondu')
    reponse17 = st.session_state.responses.get(questions[16][0], 'Non répondu')
    reponse18 = st.session_state.responses.get(questions[17][0], 'Non répondu')
    reponse19 = st.session_state.responses.get(questions[18][0], 'Non répondu')
    reponse20 = st.session_state.responses.get(questions[19][0], 'Non répondu')
    reponse21 = st.session_state.responses.get(questions[20][0], 'Non répondu')
    reponse22 = st.session_state.responses.get(questions[21][0], 'Non répondu')
    reponse23 = st.session_state.responses.get(questions[22][0], 'Non répondu')

    if reponse1 == "J'ai une idée précise de la mission de mon entreprise et de sa vision.":
        st.write("Vous avez une direction claire pour votre entreprise. Cela favorise une motivation accrue et une prise de décisions alignée sur votre objectif à long terme.")
        st.write("Continuez à communiquer cette vision à vos équipes et intégrez-la dans votre stratégie à long terme. Adaptez-la régulièrement en fonction de l’évolution du marché et des opportunités.")
    elif reponse1 == "Ma mission est claire, mais je n'ai pas encore défini ma vision à long terme.":
        st.write("Vous avez une bonne base, mais il vous manque la vision à long terme pour orienter la croissance et les décisions futures.")
        st.write(" Prenez le temps de définir une vision inspirante qui guidera votre entreprise sur plusieurs années. Posez-vous la question : Où souhaitez-vous être dans 5, 10 ou 20 ans ? Une vision claire vous aidera à structurer vos décisions et à motiver vos équipes.")
    elif reponse1 == "Je comprends l'importance de la vision mais je ne l'ai pas encore définie.":
        st.write("L'absence de vision à long terme peut nuire à la motivation de vos équipes et à l’alignement des actions.")
        st.write("Il est essentiel de formaliser votre vision pour donner une direction claire à votre entreprise. Identifiez vos ambitions à long terme et transformez-les en une déclaration inspirante qui servira de boussole stratégique.")
    elif reponse1 == "Je ne vois pas l'intérêt d'avoir une vision à long terme pour mon entreprise.":
        st.write("Ne pas avoir de vision peut entraîner une perte de direction stratégique et limiter la croissance de l’entreprise.")
        st.write("Même si cela ne semble pas prioritaire aujourd’hui, avoir une vision permet d’anticiper les défis et d’orienter votre croissance. Essayez de définir, même de manière simple, où vous aimeriez voir votre entreprise dans quelques années. Cela vous aidera à prendre des décisions plus cohérentes.")

    if reponse2 == "J'ai une compréhension claire des tendances actuelles dans mon secteur.":
        st.write("Vous êtes bien préparé et pourrez prendre des décisions stratégiques informées.")
        st.write("Continuez à surveiller activement l’évolution de votre secteur à travers des études de marché, des rapports d’analyse et des conférences. Partagez ces informations avec votre équipe pour maximiser leur impact stratégique.")
    elif reponse2 ==  "Je connais certaines tendances dans mon secteur, mais je ne suis pas sûr de leur impact.":
        st.write("Vous êtes partiellement préparé, mais vous risquez de manquer certaines opportunités ou de réagir trop tard.")
        st.write("Approfondissez votre compréhension des tendances en analysant leur impact potentiel sur votre activité. Utilisez des outils comme l’analyse SWOT, PESTEL et les 5 forces de Porter pour mieux évaluer les opportunités et menaces de votre marché.")
    elif reponse2 == "J'essaie de suivre les tendances, mais je n'ai pas une vision claire.":
        st.write("Il vous manque une vue d'ensemble claire, ce qui peut limiter votre capacité à anticiper les changements du marché.")
        st.write("Structurez votre veille stratégique en suivant des sources fiables (rapports d’experts, études sectorielles, blogs spécialisés). Utilisez des outils d'analyse comme Perplexity pour approfondir votre compréhension des tendances et identifier les signaux faibles avant qu’ils ne deviennent des bouleversements majeurs.")
    elif reponse2 == "Je n'ai pas pris le temps d'analyser les tendances de mon secteur.":
        st.write("L'ignorance des tendances peut rendre votre entreprise obsolète, car vous ne pourrez pas vous adapter aux nouvelles demandes du marché.")
        st.write("Il est essentiel de commencer dès maintenant à observer l’évolution de votre secteur. Réalisez une analyse SWOT et PESTEL pour identifier les forces, faiblesses, opportunités et menaces qui vous concernent. Servez-vous des 5 forces de Porter pour mieux comprendre la dynamique concurrentielle. Des outils comme Perplexity peuvent vous aider à obtenir rapidement des informations pertinentes.")

    if reponse3 == "Ma proposition de valeur est claire et me différencie bien de la concurrence.":
        st.write("Vous êtes bien positionné sur le marché avec une offre unique et attrayante.")
        st.write("Continuez à affiner votre proposition en restant à l’écoute de vos clients et des évolutions du marché. Assurez-vous qu’elle est bien communiquée sur tous vos supports (site web, réseaux sociaux, argumentaire commercial) pour maximiser son impact.")
    elif reponse3 == "J'ai une proposition de valeur, mais elle pourrait être affinée pour mieux me différencier.":
        st.write("Vous êtes sur la bonne voie, mais un affinement de votre proposition peut vous permettre de mieux vous démarquer.")
        st.write("Analysez ce qui vous rend unique par rapport à vos concurrents. Utilisez une matrice de différenciation ou une analyse concurrentielle pour identifier les éléments à renforcer. Testez votre message auprès de vos clients pour voir ce qui résonne le plus.")
    elif reponse3 == "Je sais que j'ai besoin d'une proposition de valeur, mais je ne l'ai pas encore définie.":
        st.write("Ne pas avoir une proposition claire vous rend moins compétitif et peut entraîner la confusion chez vos clients.")
        st.write("Définissez votre proposition de valeur unique (PVU) en vous posant trois questions clés : Quel problème résolvez-vous ? Pour qui ? Pourquoi votre solution est-elle meilleure que celle des concurrents ? Utilisez une analyse concurrentielle et le canvas de proposition de valeur pour formaliser une offre claire et percutante.")
    elif reponse3 == "Je ne vois pas ce que c'est qu'une proposition de valeur.":
        st.write("Sans proposition de valeur, vous risquez de perdre des opportunités clients au profit de la concurrence.")
        st.write("Une proposition de valeur est ce qui vous distingue et donne envie aux clients de choisir votre produit ou service. Identifiez ce qui fait votre force en comparant votre offre à celle de vos concurrents. Inspirez-vous d’exemples réussis dans votre secteur et formalisez une phrase simple qui explique en quoi vous êtes unique.")

    if reponse4 == "J’ai une grille tarifaire claire, permettant une marge confortable.":
        st.write("Vous offrez une transparence totale, ce qui renforce la confiance et la fidélité de vos clients.")
        st.write("Continuez à surveiller régulièrement votre positionnement tarifaire en fonction de la concurrence et des attentes du marché. Pensez à ajuster vos prix en fonction de la valeur perçue et des évolutions économiques (inflation, coût des matières premières, etc.).")
    elif reponse4 == "Ma grille tarifaire existe, mais ne marge pas assez.":
        st.write("Vous devez simplifier votre grille tarifaire pour améliorer la compréhension et la transparence.")
        st.write("Analysez vos coûts et votre valeur ajoutée pour ajuster vos prix sans impacter négativement votre clientèle. Étudiez les prix du marché avec des comparateurs de prix et envisagez une stratégie de montée en gamme ou d’optimisation des coûts pour améliorer votre rentabilité.")
    elif reponse4 == "J’ai une grille tarifaire, mais elle est complexe et pas toujours cohérente.":
        st.write("Une grille tarifaire complexe peut créer de la confusion chez vos clients et nuire à la satisfaction.")
        st.write("Simplifiez votre offre en réduisant le nombre d’options inutiles et en structurant votre tarification de manière intuitive. Optez pour une communication tarifaire claire et accessible, en mettant en avant les bénéfices de chaque niveau de prix pour éviter la confusion.")
    elif reponse4 == "Je n’ai pas de grille tarifaire clairement définie.":
        st.write("L’absence d’une grille tarifaire claire peut entraîner des inégalités et des conflits avec vos clients.")
        st.write("Élaborez une grille tarifaire structurée et transparente, en définissant des prix cohérents avec la valeur perçue de vos services/produits. Utilisez des outils comme les comparateurs de prix et analysez la concurrence pour vous positionner efficacement tout en garantissant une rentabilité suffisante.")
    
    if reponse5 == "J’ai une vision claire de la rentabilité de chaque produit/service. Je suis en mesure d’ajuster les prix ou les coûts en fonction des marges.":
        st.write("Vous optimisez vos prix et coûts pour maximiser la rentabilité.")
        st.write("Continuez à suivre régulièrement vos marges et ajustez-les en fonction des variations du marché (coût des matières premières, concurrence, demandes clients). Pensez aussi à identifier les opportunités d’amélioration de vos coûts de production ou de prestation.")
    elif reponse5 == "Je connais globalement les marges, mais il me manque des outils pour un suivi précis et régulier.":
        st.write("Vous manquez d’outils pour une gestion optimale de la rentabilité, ce qui peut affecter vos résultats.")
        st.write("Mettez en place un tableau de bord de suivi des marges et utilisez un logiciel ERP ou un outil comptable pour suivre en détail la rentabilité de chaque produit/service. Un suivi plus précis vous permettra d’ajuster vos décisions stratégiques et d’améliorer votre rentabilité.")
    elif reponse5 == "Je ne suis pas vraiment certain des marges de chaque produit/service. Je n’ai pas de système en place pour suivre les rentabilités de manière détaillée.":
        st.write("Sans un suivi détaillé, vous risquez de ne pas identifier les produits non rentables et de gaspiller des ressources.")
        st.write("Il est essentiel d’établir un système de suivi des marges. Commencez par analyser vos coûts fixes et variables, puis utilisez un logiciel de gestion ou un simple tableau Excel pour suivre vos marges produit par produit. Cela vous aidera à repérer les offres les moins rentables et à ajuster vos stratégies tarifaires.")
    
    if reponse6 == "J'ai des actions marketing efficaces pour attirer mes prospects et je les analyse régulièrement.":
        st.write("Vous maximisez vos performances marketing et optimisez votre taux de conversion.")
        st.write("Continuez à surveiller vos performances avec des outils comme Google Analytics, Meta Business Suite ou un CRM comme Odoo. Testez différentes approches, optimisez vos campagnes et adaptez votre contenu en fonction des retours et des tendances du marché.")
    elif reponse6 == "Je mets en place des actions marketing, mais je n’évalue pas toujours leur efficacité.":
        st.write("Faibles résultats marketing, manque de conversion.")
        st.write("Mettez en place un suivi de vos performances à l’aide de KPIs clés (taux de conversion, trafic web, engagement sur les réseaux sociaux). Utilisez Google Analytics, Facebook Insights ou un CRM pour mesurer et ajuster vos actions marketing en fonction des résultats obtenus.")
    elif reponse6 == "J’ai quelques actions marketing, mais elles sont dispersées et peu structurées.":
        st.write("Manque de visibilité auprès de votre public cible.")
        st.write("Structurez votre plan marketing en définissant des objectifs clairs et en coordonnant vos actions. Un marketing incohérent peut empêcher votre audience de comprendre votre message et d’interagir avec votre marque.")
    elif reponse6 == "Je ne mets pas en place de stratégie pour attirer mes prospects.":
        st.write("Faible taux de conversion et perte de prospects.")
        st.write("Il est essentiel de créer une stratégie marketing digitale pour générer des leads et convertir vos prospects en clients. Investissez dans le SEO pour améliorer la visibilité de votre site web. Utilisez les réseaux sociaux pour engager votre audience et attirer des prospects qualifiés. Créez du contenu pertinent (articles, vidéos, webinaires) répondant aux besoins de votre cible. Mettez en place des campagnes publicitaires ciblées pour booster votre visibilité et vos conversions.")
    
    if reponse7 == "Je sais exactement ce qui rend mon produit ou service unique et je le mets en avant.":
        st.write("Vous maximisez votre impact sur votre marché et renforcez votre image de marque.")
        st.write("Continuez à valoriser vos atouts en les intégrant à toutes vos communications (site web, réseaux sociaux, publicité). Restez à l’écoute des tendances et ajustez vos différenciateurs si nécessaire pour garder une longueur d’avance sur la concurrence.")
    elif reponse7 == "J'ai quelques éléments différenciateurs, mais je pourrais les exploiter davantage.":
        st.write("Votre produit/service risque de passer inaperçu face à la concurrence.")
        st.write("Affinez et valorisez davantage vos éléments différenciateurs pour vous démarquer clairement. Une différenciation floue peut réduire votre impact commercial et votre attractivité.")
    elif reponse7 == "Je n’ai pas encore identifié ce qui rend mon produit/service exceptionnel.":
        st.write("Les clients ne verront pas de raison de choisir votre produit/service plutôt qu’un autre.")
        st.write("Il est essentiel de définir votre proposition de valeur pour ne pas être noyé dans la masse. Un produit/service sans différenciation a du mal à convaincre et à fidéliser.")
    elif reponse7 == "Je ne vois pas l'importance de différencier mon produit/service.":
        st.write("Une offre peu distinctive peut entraîner des problèmes de fidélisation et une perte de clients.")
        st.write("Sans différenciation, votre produit/service devient interchangeable, ce qui peut réduire vos marges et limiter votre croissance. Il est crucial de mettre en avant des éléments qui vous rendent unique.")
    
    if reponse8 == "J'ai mis en place des actions concrètes et régulières pour fidéliser mes clients.":
        st.write("Vous maintenez un bon taux de fidélisation et réduisez vos coûts d'acquisition en transformant vos clients en ambassadeurs.")
        st.write("Continuez à améliorer votre programme de fidélisation en analysant son efficacité et en innovant pour garder un avantage concurrentiel.")
    elif reponse8 == "Je suis en train de développer des actions pour fidéliser mes clients, mais elles ne sont pas encore structurées.":
        st.write("Les clients reviendront moins souvent, ce qui augmentera votre coût d’acquisition global.")
        st.write("Structurez et formalisez vos actions de fidélisation pour assurer un impact durable. Sans cadre défini, vos efforts risquent de ne pas être efficaces sur le long terme.")
    elif reponse8 == "J'ai des clients fidèles, mais je n'ai pas de programme dédié pour les fidéliser.":
        st.write("Une mauvaise gestion de la fidélisation peut entraîner une diminution des ventes récurrentes.")
        st.write("Capitalisez sur vos clients existants en créant un programme de fidélité structuré. Même si certains reviennent naturellement, un programme dédié renforcera leur engagement et augmentera leur fréquence d’achat.")
    elif reponse8 == "Je ne mets pas l'accent sur la fidélisation de mes clients.":
        st.write("Un faible taux de fidélisation peut nuire à la réputation de votre entreprise, car les clients insatisfaits partent à la concurrence.")
        st.write("Investissez dans une stratégie de fidélisation pour limiter la perte de clients et maximiser la valeur à long terme de chaque client.")
    
    if reponse9 == "J’utilise un CRM efficace pour suivre mes prospects et clients.":
        st.write("Vous optimisez votre gestion de la relation client, améliorez la personnalisation et augmentez vos conversions.")
        st.write("Continuez à maximiser l'utilisation de votre CRM en explorant ses fonctionnalités avancées pour affiner encore votre gestion des prospects et de la fidélisation.")
    elif reponse9 == "J’utilise un CRM, mais je ne l’exploite pas pleinement.":
        st.write("Vous n’aurez pas une vue claire sur les interactions et les préférences de chaque client.")
        st.write("Exploitez pleinement votre CRM pour avoir une vision complète et actualisée de vos prospects et clients. L'optimisation de votre CRM est essentielle pour améliorer l'efficacité de votre équipe commerciale et maximiser vos ventes.")
    elif reponse9 == "Je sais qu’un CRM pourrait m’aider, mais je ne l’ai pas encore mis en place.":
        st.write("Vous risquez de manquer des opportunités de vente ou d'engagement avec des prospects déjà intéressés.")
        st.write("Mettez en place un CRM pour automatiser et améliorer le suivi de vos prospects et clients. Cela vous permettra de centraliser toutes les informations et d'augmenter l'efficacité de votre processus commercial.")
    elif reponse9 == "Je ne vois pas l’intérêt d’utiliser un CRM.":
        st.write("Le suivi manuel est long, sujet aux erreurs et réduit l'efficacité de votre équipe commerciale.")
        st.write("Implémentez un CRM pour faciliter la gestion des prospects et clients. Sans CRM, il est difficile de suivre l'ensemble des interactions et d’optimiser la conversion des prospects.")
    
    if reponse10 == "L’équipe possède toutes les compétences nécessaires et chaque membre est parfaitement adapté à son rôle.":
        st.write("L’équipe est performante et travaille efficacement, sans obstacles majeurs liés aux compétences.")
        st.write("Continuez à renforcer vos compétences existantes en offrant des formations continues pour rester à la pointe dans vos domaines d'expertise. Cela garantit que l’équipe reste agile face aux évolutions du marché.")
    elif reponse10 == "L’équipe est compétente, mais quelques domaines clés nécessitent des améliorations.":
        st.write("Des lacunes dans certaines compétences peuvent entraîner des retards et affecter la performance globale.")
        st.write("Identifiez les domaines spécifiques nécessitant des améliorations et mettez en place un plan de formation ciblé pour combler ces lacunes. Cela renforcera l'efficacité de l’équipe.")
    elif reponse10 == "L’équipe manque de compétences dans certains domaines spécifiques, ce qui crée des obstacles.":
        st.write("Les lacunes de compétences peuvent entraîner des frustrations et des retards dans l'exécution des projets, ce qui peut affecter la motivation et la productivité.")
        st.write("Comblez les lacunes en compétences par des formations ciblées et des ressources externes (comme des experts ou des consultants) pour résoudre les obstacles spécifiques.")
    elif reponse10 == "Il y a un manque important de compétences clés dans l’équipe, affectant la performance globale.":
        st.write("Le manque de compétences clés risque de nuire gravement à la performance et à l'efficacité de l'équipe. Cela peut également affecter la motivation des employés.")
        st.write("Formez votre équipe en priorité sur les compétences essentielles à la performance de l’entreprise. Mettez en place une stratégie de développement des compétences à long terme pour pallier ces manques.")

    if reponse11 == "J’ai des KPIs clairs et je les suis régulièrement pour ajuster ma stratégie.":
        st.write("Vous avez une vision claire de vos performances et vous pouvez optimiser vos actions en temps réel.")
        st.write("Continuez à suivre vos KPIs avec rigueur et ajustez votre stratégie en fonction des résultats. La régularité dans le suivi est essentielle pour rester compétitif.")
    elif reponse11 == "J’ai quelques KPIs définis, mais je ne les analyse pas systématiquement.":
        st.write("Vous n’aurez pas une vision claire de l'efficacité de vos actions commerciales, ce qui rend difficile l'optimisation de vos efforts.")
        st.write("Intégrez l’analyse régulière de vos KPIs pour pouvoir réagir rapidement aux évolutions et ajuster votre stratégie en fonction des données.")
    elif reponse11 == "Je n’ai pas encore de KPIs précis pour mesurer ma performance.":
        st.write("Sans KPIs, vous risquez de ne pas réagir rapidement aux problèmes ou de manquer des opportunités d'amélioration.")
        st.write("Mettez en place des KPIs précis dès que possible pour avoir une mesure objective de votre performance commerciale. Cela vous permettra de rester proactif et d’optimiser vos efforts.")
    elif reponse11 == "Je ne vois pas l’utilité de suivre des KPIs.":
        st.write("Une stratégie commerciale mal définie entraînera une perte de direction dans vos efforts de vente.")
        st.write("Implémentez des KPIs dès maintenant pour obtenir des insights précieux sur votre activité et améliorer la gestion de votre stratégie commerciale. Sans cela, vous risquez de naviguer sans boussole.")
    
    if reponse12 == "L'organisation interne de l'entreprise est claire et bien structurée, facilitant la communication entre collègues et dirigeants et la prise de décision.":
        st.write("Une organisation bien structurée favorise une communication fluide et une prise de décision rapide et efficace.")
        st.write("Continuez à maintenir une organisation claire et structurée. Pour renforcer cette organisation, veillez à réévaluer régulièrement les rôles et la répartition des tâches pour rester aligné sur les objectifs à long terme.")
    elif reponse12 == "L'organisation est en place, mais manque de certaines clarifications ou alignements au sein des équipes.":
        st.write("Une mauvaise communication interne peut entraîner des retards dans la prise de décision et des divergences sur les priorités.")
        st.write("Clarifiez les rôles et les responsabilités pour améliorer l'alignement et la communication. Cela réduira les ambiguïtés et aidera à mieux coordonner les actions au sein des équipes.")
    elif reponse12 == "Il y a des ambiguïtés dans l'organisation, créant des zones de confusion.":
        st.write("La confusion des rôles et des responsabilités peut entraîner une mauvaise exécution des tâches, ce qui diminue l’efficacité globale.")
        st.write("Clarifiez immédiatement les responsabilités au sein de chaque équipe pour réduire les zones de confusion. L’organisation doit être parfaitement alignée pour améliorer l'efficacité et la coordination des équipes.")
    elif reponse12 == "L'organisation est chaotique, entraînant des décisions mal informées et une communication inefficace.":
        st.write("La désorganisation générale peut entraîner des erreurs dans les décisions et une perte de temps, nuisant à la performance globale de l'entreprise.")
        st.write("Réorganisez votre structure interne pour garantir une meilleure gestion des processus et une communication fluide. Cela vous permettra de prendre des décisions plus éclairées et d'améliorer l'efficacité.")
     
    if reponse13 == "Tous les processus sont optimisés et automatisés pour améliorer l’efficacité.":
        st.write("L'optimisation et l'automatisation des processus permettent de gagner en efficacité, réduire les erreurs humaines et améliorer la qualité du travail.")
        st.write("Continuez à améliorer les processus existants pour maintenir cette performance élevée. Évaluez régulièrement les processus pour repérer de nouvelles opportunités d’automatisation ou d’optimisation.")
    elif reponse13 == "Les processus sont relativement optimisés, mais certains aspects peuvent encore être améliorés.":
        st.write("Les processus partiellement optimisés peuvent engendrer des inefficacités, des coûts supplémentaires et ralentir la productivité globale.")
        st.write("Identifiez les points faibles et mettez en œuvre des outils ou des stratégies pour automatiser ou simplifier les processus restants. Cela maximisera la productivité et réduira les coûts inutiles.")
    elif reponse13 == "De nombreux processus sont inefficaces et ralentissent les opérations.":
        st.write("Les processus inefficaces créent des retards, des erreurs fréquentes et des gaspillages de ressources, ce qui entraîne une baisse de la productivité et de la qualité.")
        st.write("Réorganisez et automatisez les processus clés pour améliorer l'efficacité. L'optimisation de ces processus est essentielle pour réduire le gaspillage de temps et d’énergie.")
    elif reponse13 == "Il y a un grand nombre de processus obsolètes ou mal gérés, provoquant des retards et des erreurs.":
        st.write("La gestion d'un grand nombre de processus obsolètes entraîne des erreurs fréquentes, des retards dans l'exécution des tâches, et une perte importante de ressources.")
        st.write("Réalisez un audit complet de vos processus pour éliminer les obsolètes et mettre en place des solutions d’automatisation ou d’optimisation modernes.")
    
    if reponse14 == "L'équipe est motivée, performante et réalise les objectifs fixés avec enthousiasme.":
        st.write("Une équipe motivée et performante génère des résultats positifs, une cohésion forte et une culture d’entreprise saine.")
        st.write("Maintenez cet élan en continuant à offrir des opportunités de développement personnel, à reconnaître les efforts individuels et collectifs, et à maintenir un environnement de travail stimulant.")
    elif reponse14 == "L'équipe est généralement motivée, mais il y a quelques fluctuations dans la productivité.":
        st.write("Des fluctuations de motivation peuvent entraîner des baisses temporaires de productivité, affectant l’atteinte des objectifs sur le long terme.")
        st.write("Instaurer des pratiques régulières de feedback et ajuster les objectifs ou la charge de travail pour maintenir une motivation stable.")
    elif reponse14 == "La motivation est inégale, ce qui génère des périodes de faible productivité.":
        st.write("Une motivation inégale crée une instabilité dans la performance, avec des périodes de sous-performance qui peuvent affecter la productivité de l’ensemble de l’équipe.")
        st.write("Renforcez les actions de motivation ciblée et mettez en place des programmes de reconnaissance pour encourager la performance constante.")

    if reponse15 == " Il n'y a pas de personnes irremplaçables, car nous avons une bonne répartition des compétences et des connaissances.":
        st.write("La bonne répartition des compétences garantit la continuité des opérations et réduit les risques associés à la dépendance à une seule personne.")
        st.write("Continuez à maintenir une équipe polyvalente, encouragez le partage de connaissances et continuez à documenter les processus pour maintenir la stabilité à long terme.")
    elif reponse15 == "Nous avons identifié des personnes clés, mais nous travaillons à réduire cette dépendance.":
        st.write("Bien que des actions soient en cours pour réduire la dépendance, la perte de ces personnes clés pourrait encore perturber les opérations.")
        st.write("Accélérez le processus de transfert de compétences et établissez des plans de succession clairs pour atténuer tout risque potentiel.")
    elif reponse15 == "Il y a quelques personnes clés, mais nous avons des plans de contingence en place.":
        st.write("Bien que des plans de contingence soient en place, la perte de personnes clés pourrait entraîner une perte de connaissances et d’expertise, affectant les opérations.")
        st.write("Renforcez encore davantage les plans de contingence et assurez-vous que les processus critiques sont bien documentés et partagés.")
    elif reponse15 == "Oui, certaines personnes sont cruciales et leur départ pourrait impacter fortement l’entreprise.":
        st.write("La perte de ces personnes clés pourrait entraîner des perturbations importantes dans les opérations et entraîner la perte de connaissances stratégiques.")
        st.write("Établissez des plans de succession urgents et veillez à ce que toutes les connaissances critiques soient transférées pour éviter les risques d’inefficacité.")
    
    if reponse16 == "Un système de gestion des savoirs est en place, permettant de partager facilement les connaissances au sein de l’entreprise.":
        st.write("Vous avez un système robuste en place, ce qui permet de préserver les connaissances clés et de faciliter le travail de l'équipe.")
        st.write("Maintenez et optimisez ce système pour garantir un partage fluide et une évolution continue des connaissances.")
    elif reponse16 == "Il existe un début de gestion des savoirs, mais certains éléments importants sont encore dispersés.":
        st.write("Le manque de centralisation des informations importantes peut entraîner des inefficacités, notamment pour les nouveaux employés ou en cas de départs d’experts.")
        st.write("Consolidez et centralisez les savoirs clés dans un système structuré pour garantir un partage fluide des informations.")
    elif reponse16 == "Il y a une perte de savoirs clés au sein de l’équipe, avec un manque de partage d’informations.":
        st.write("Ce manque de gestion des savoirs peut entraîner des erreurs, des inefficacités et des difficultés pour les nouveaux membres de l’équipe.")
        st.write("Mettez en place un système de gestion des savoirs dès que possible, avec un processus pour assurer le partage continu d'informations et la conservation des savoirs clés.")
    elif reponse16 == "Il n'y a pas de gestion des savoirs, ce qui conduit à la perte d'expertise et à l’inefficacité.":
        st.write("L’absence de gestion des savoirs peut entraîner des risques importants de perte de compétences et d'expertise, avec des conséquences sur l’efficacité de l’entreprise.")
        st.write("Implémentez immédiatement un système de gestion des savoirs pour éviter la perte de connaissances et renforcer l’efficacité de l’équipe.")

    if reponse17 == "Les rôles et responsabilités de chaque membre de l’équipe sont parfaitement définis et bien compris.":
        st.write("L’équipe est bien structurée, ce qui permet une exécution efficace des tâches et une absence de confusion.")
        st.write("Maintenez cette clarté en veillant à faire une réévaluation régulière des rôles et des responsabilités.")
    elif reponse17 == "Les rôles sont définis, mais il y a quelques ambiguïtés sur certaines responsabilités.":
        st.write("Des ambiguïtés sur les responsabilités peuvent entraîner des malentendus et une exécution incohérente des tâches.")
        st.write("Clarifiez les zones d’ambiguïté en révisant les rôles et responsabilités et en utilisant des outils de gestion comme la matrice RACI.")
    elif reponse17 == "Certains rôles sont flous, ce qui entraîne des zones de confusion au sein de l’équipe.":
        st.write("La confusion sur les rôles peut conduire à des erreurs, des conflits internes, et une mauvaise exécution des tâches.")
        st.write("Clarifiez les rôles et responsabilités de façon urgente et mettez en place des outils de gestion tels que la matrice RACI pour éviter les malentendus.")
    elif reponse17 == "Il n'y a aucune clarté sur les rôles et responsabilités, ce qui mène à des conflits et erreurs internes.":
        st.write("L’absence de clarté entraîne des conflits, des erreurs fréquentes et une mauvaise exécution des tâches, impactant négativement l’équipe et l’entreprise.")
        st.write("Clarifiez immédiatement les rôles et responsabilités, en utilisant des outils de gestion comme la matrice RACI et en assurant une communication continue.")
    
    if reponse18 == "La rentabilité est suivie de manière régulière grâce à un tableau de bord financier clair.":
        st.write("Une bonne visibilité sur les marges et les performances financières, permettant une gestion financière optimisée.")
        st.write("Maintenez ce suivi régulier et optimal pour assurer une rentabilité constante et pour anticiper les évolutions financières.")
    elif reponse18 == "Un suivi est en place, mais il manque certaines informations pour une évaluation complète de la rentabilité.":
        st.write("Des décisions financières peuvent être prises sur des bases incomplètes, ce qui peut affecter la rentabilité à long terme.")
        st.write("Complétez votre tableau de bord financier pour inclure tous les éléments essentiels de rentabilité et obtenez des outils fiables pour une évaluation plus complète.")
    elif reponse18 == "La rentabilité est parfois suivie, mais de manière désorganisée et peu fiable.":
        st.write("Une gestion financière inefficace peut entraîner des erreurs et des retards dans la détection des problèmes de rentabilité, ce qui pourrait avoir un impact majeur.")
        st.write("Mettez en place un suivi structuré et fiable de la rentabilité pour éviter les erreurs et prendre des décisions éclairées.")
    elif reponse18 == "Il n’y a pas de suivi systématique de la rentabilité, ce qui entraîne des erreurs dans la gestion financière.":
        st.write("Un manque de suivi peut mener à des problèmes financiers importants avant qu’ils ne soient détectés, nuisant ainsi à la rentabilité globale de l’entreprise.")
        st.write("Établissez un suivi régulier et structuré de la rentabilité en mettant en place un tableau de bord financier détaillé et un ERP.")

    if reponse19 == "La trésorerie est gérée efficacement avec des prévisions claires et une bonne visibilité.":
        st.write("La gestion de la trésorerie est optimisée, avec une bonne visibilité des flux de liquidités, permettant de prendre des décisions éclairées.")
        st.write("Maintenez cette gestion proactive de la trésorerie en révisant régulièrement vos prévisions et en continuant à surveiller vos flux de trésorerie pour garantir la stabilité financière de l'entreprise.")
    elif reponse19 == "Un plan de trésorerie est en place, mais les prévisions ne sont pas toujours révisées régulièrement.":
        st.write("Un manque de révisions régulières des prévisions peut entraîner des imprévus ou une mauvaise gestion des liquidités, mettant l'entreprise en difficulté.")
        st.write("Mettez en place un processus de révision régulière de votre plan de trésorerie pour garantir que les prévisions sont toujours à jour et pertinentes.")
    elif reponse19 == "La gestion de la trésorerie est partiellement optimisée, mais certaines informations cruciales manquent.":
        st.write(" L'absence d'informations financières cruciales peut créer des tensions sur les liquidités et des difficultés pour financer les projets ou investissements à venir.")
        st.write("Optimisez la gestion de la trésorerie en collectant toutes les informations financières nécessaires pour avoir une visibilité complète sur vos flux de trésorerie et les prévisions.")
    elif reponse19 == "La trésorerie est mal gérée, avec des imprévus fréquents affectant la liquidité de l’entreprise.":
        st.write("Une gestion de trésorerie inefficace peut entraîner un manque de liquidités pour faire face aux besoins à court terme, ce qui expose l'entreprise à des risques financiers importants.")
        st.write("Établissez un plan de gestion de trésorerie clair et régulier, en mettant l'accent sur les prévisions à court et long terme pour éviter les tensions financières.")
    
    if reponse20 == "Les risques financiers sont clairement identifiés et des stratégies de prévention sont en place.":
        st.write("Vous avez une gestion proactive des risques financiers, ce qui protège l'entreprise des pertes majeures et permet de prendre des décisions éclairées.")
        st.write("Continuez à évaluer et à réajuster régulièrement vos stratégies de couverture des risques financiers pour garantir la stabilité à long terme de votre entreprise.")
    elif reponse20 == "Certains risques sont identifiés, mais des stratégies de couverture sont encore à mettre en place.":
        st.write("Bien que certains risques soient identifiés, l'absence de stratégies de couverture expose l'entreprise à des conséquences financières en cas de crise ou de mauvais choix.")
        st.write("Identifiez tous les risques financiers majeurs et développez des stratégies pour les couvrir efficacement afin de réduire la vulnérabilité de votre entreprise.")
    elif reponse20 == "Les risques financiers sont partiellement identifiés, mais aucun plan de gestion n’est instauré.":
        st.write("L'absence de plan de gestion des risques financiers augmente le risque de pertes imprévues et de mauvaise gestion des finances de l'entreprise.")
        st.write("Élaborez un plan de gestion des risques financiers en identifiant les risques majeurs et en mettant en place des stratégies pour y faire face.")
    elif reponse20 == "Les risques financiers ne sont pas identifiés ni gérés, créant une vulnérabilité à des pertes majeures.":
        st.write("L'absence de gestion des risques financiers peut entraîner des pertes importantes et mettre l'entreprise en danger, notamment en cas de retournement du marché ou de décisions financières mal orientées.")
        st.write(" Mettez en place une stratégie de gestion des risques financiers pour identifier les risques potentiels et définir des plans d’action en cas de crise.")
    
    if reponse21 == "Un plan de financement solide est en place pour soutenir la croissance de l’entreprise.":
        st.write("Vous êtes bien préparé pour financer la croissance et les projets stratégiques à long terme. Cela vous permet de saisir des opportunités tout en limitant les risques financiers.")
        st.write("Continuez à suivre et ajuster régulièrement votre plan de financement pour vous assurer qu’il reste aligné avec la stratégie de croissance de l’entreprise.")
    elif reponse21 == "Le plan de financement existe, mais il manque de flexibilité pour faire face à des imprévus.":
        st.write("Le manque de flexibilité pourrait limiter votre capacité à réagir face à des imprévus ou à saisir des opportunités de croissance inattendues.")
        st.write("Améliorez la flexibilité de votre plan de financement en intégrant des options de financement plus adaptables à vos besoins.")
    elif reponse21 == "Un plan de financement partiel est en place, mais il ne couvre pas tous les besoins de l’entreprise.":
        st.write("L'absence de financement pour certains besoins peut freiner votre croissance ou créer des difficultés pour soutenir certains projets clés.")
        st.write("Élargissez votre plan de financement pour couvrir tous les besoins stratégiques de l’entreprise, en prenant en compte la croissance à court, moyen et long terme.")
    elif reponse21 == "L’entreprise n’a pas de plan de financement clairement défini, ce qui limite les possibilités de croissance.":
        st.write("L'absence de plan de financement clairement défini empêche l'entreprise de saisir des opportunités et peut entraîner une gestion financière désorganisée.")
        st.write("Élaborez un plan de financement détaillé qui prévoit tous les besoins de l’entreprise et offre des solutions de financement diversifiées.")
    
    if reponse22 == "Le tableau de bord financier inclut des indicateurs clairs tels que la marge brute, la marge nette, et les ratios de rentabilité.":
        st.write("Vous avez une vision claire de la performance financière de votre entreprise, ce qui vous permet de prendre des décisions éclairées et d'optimiser vos stratégies.")
        st.write("Maintenez ce tableau de bord à jour et élargissez-le pour inclure d'autres indicateurs si nécessaire pour une analyse encore plus détaillée.")
    elif reponse22 == "Les indicateurs financiers sont suivis de manière partielle, mais manquent d’informations essentielles pour une analyse complète.":
        st.write("L'absence d'une vue complète de la rentabilité peut mener à des décisions mal informées et à des opportunités manquées pour améliorer la performance financière.")
        st.write("Complétez votre tableau de bord financier en incluant tous les indicateurs nécessaires à une analyse complète de votre rentabilité.")
    elif reponse22 == "Il existe quelques indicateurs financiers, mais ils ne sont pas utilisés de manière cohérente.":
        st.write("L'incohérence dans le suivi des indicateurs financiers peut réduire la fiabilité des données, rendant difficile l'évaluation de la performance ou l'identification de problèmes.")
        st.write("Rationalisez l’utilisation des indicateurs financiers en vous assurant qu'ils sont suivis de manière régulière et cohérente.")
    elif reponse22 =="Aucun tableau de bord financier n’est mis en place pour suivre les indicateurs clés de rentabilité, ce qui entraîne des décisions mal informées.":
        st.write("L'absence d’un tableau de bord financier limite votre capacité à évaluer la rentabilité et à optimiser la gestion financière, augmentant le risque de mauvaises décisions.")
        st.write("Mettez en place un tableau de bord financier complet pour suivre toutes les informations pertinentes et prendre des décisions éclairées.")
    
    if reponse23 == "Un suivi rigoureux des créances clients est mis en place avec un contrôle des délais de paiement.":
        st.write("Vous avez une bonne gestion des créances, ce qui assure une meilleure trésorerie et de bonnes relations avec vos clients.")
        st.write("Maintenez un suivi rigoureux et continuez à utiliser des outils ERP pour automatiser la gestion des créances clients.")
    elif reponse23 == "Le suivi des créances est partiellement en place, mais il manque de rigueur pour éviter les impayés.":
        st.write("Des retards de paiement peuvent encore se produire, ce qui peut entraîner des tensions financières et affecter votre trésorerie.")
        st.write("Renforcez la rigueur du suivi des créances clients pour éviter les retards de paiement et garantir une trésorerie saine.")
    elif reponse23 == "Il existe un suivi sporadique des créances, mais les délais sont souvent ignorés.":
        st.write("Les créances en retard risquent d'augmenter, ce qui peut provoquer une crise de trésorerie et impacter vos obligations financières.")
        st.write("Mettez en place un suivi systématique et structuré des créances pour réduire les risques de retard de paiement et améliorer votre liquidité.")
    elif reponse23 == "Aucune gestion régulière des créances clients, entraînant des problèmes de liquidité.":
        st.write("Le manque de gestion des créances peut entraîner une grave crise de trésorerie, des tensions avec les clients et des difficultés à honorer vos obligations financières.")
        st.write("Mettez en place une gestion régulière et rigoureuse des créances clients, en intégrant un suivi dans votre ERP.")

    
    st.write("---")  
    st.write("Version avec formulaire et et retour réalisé par ChatGPT :") 

    # api_key = os.getenv("OPENAI_API_KEY")
    # Configuration de l'API OpenAI (assurez-vous d'utiliser une variable d'environnement pour la clé API)
    # client = openai.OpenAI(api_key=api_key)

    api_key = st.secrets["OPENAI_API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    # Titre de l'application
    st.title("Génération de Synthèse Odoo")

    # Formulaire de saisie des informations utilisateur
    with st.form("contact_form"):
        prenom = st.text_input("Prénom", placeholder="Votre prénom")
        nom = st.text_input("Nom", placeholder="Votre nom")
        telephone = st.text_input("Numéro de téléphone", placeholder="Votre numéro de téléphone")
        email = st.text_input("Adresse mail", placeholder="Votre adresse email")
        content = st.text_input("content prompt",placeholder="content prompt")
        prompt1 = st.text_input("Prompt chat gpt",placeholder="Prompt chat gpt")
        submit_button = st.form_submit_button("Obtenir la synthèse")

    # Vérification des champs et génération de la synthèse
    if submit_button:
        if not prenom or not nom or not telephone or not email or not content or not prompt1:
            st.error("Veuillez remplir tous les champs du formulaire.")
        else:
            # Concaténation des réponses (exemple, les réponses doivent être définies dans votre contexte)
            reponses = "\n".join([eval(f"reponse{i}") for i in range(1, 24)])

            # Création du prompt avec le prénom du demandeur
            prompt = f"""
            {prompt1} Parlez directement à la personne en utilisant son prénom : {prenom}.
            Voici quelques éléments de contexte :
            {reponses}
            """
            
            # Fonction pour obtenir une réponse de ChatGPT
            def get_chatgpt_response(prompt):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": content},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            # Appel de l'API
            synthese = get_chatgpt_response(prompt)
            
            # Affichage du résultat
            st.subheader("Synthèse générée :")
            st.write(synthese)
