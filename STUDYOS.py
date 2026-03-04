#!/usr/bin/env python3
"""
StudyOS — Multi-Exam Study Platform (JEE, NEET, UPSC, CAT, GATE, CLAT, SSC, Banking)
Run: python3 STUDYOS.py  →  opens at http://localhost:8765
All data stored in jeeos.db (SQLite)
"""
import json, os, sys, sqlite3, hashlib, secrets, datetime, base64, io, threading, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8765
DB   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jeeos.db")

# ═══════════════════════════════════════════════════════════════════════
# EXAM DATA
# ═══════════════════════════════════════════════════════════════════════
EXAMS = {
  "JEE":{
    "name":"JEE (Mains + Advanced)","icon":"⚡","brand":"JEE","brandHL":"OS",
    "tagline":"IIT / NIT Entrance Preparation",
    "tiers":[[99,"🏆 IIT Top 100"],[95,"⭐ IIT Zone"],[85,"✅ NIT Tier-1"],[0,"📈 Keep Pushing"]],
    "subjects":{
      "Physics":{"color":"#6366f1","icon":"⚛","topics":["Mechanics","Kinematics","Rotational Motion","Gravitation","Thermodynamics","Electrostatics","Current Electricity","Magnetism","EMI","Optics","Modern Physics","Waves"]},
      "Chemistry":{"color":"#f97316","icon":"⬡","topics":["Mole Concept","Atomic Structure","Chemical Bonding","Thermodynamics","Equilibrium","Electrochemistry","Organic Basics","Hydrocarbons","Aldehydes & Ketones","Coordination Chemistry","p-Block","d-Block"]},
      "Maths":{"color":"#8b5cf6","icon":"∑","topics":["Limits & Continuity","Differentiation","Integration","Differential Equations","Matrices","Determinants","Vectors","3D Geometry","Probability","Complex Numbers","Conic Sections","Trigonometry"]},
    },
    "subtopics":{
      "Physics::Mechanics":["Newton's Laws","Work-Energy Theorem","Conservation of Momentum","Friction","Circular Motion","Centre of Mass","Spring-Mass Systems"],
      "Physics::Kinematics":["1D Motion","2D Projectile","Relative Motion","Graphs (v-t, x-t)","Uniform Circular Motion"],
      "Physics::Rotational Motion":["Moment of Inertia","Torque","Angular Momentum","Rolling Motion","Parallel Axis Theorem"],
      "Physics::Gravitation":["Kepler's Laws","Gravitational Potential","Orbital Velocity","Escape Velocity","Satellites"],
      "Physics::Thermodynamics":["Zeroth Law","First Law","PV Diagrams","Carnot Cycle","Entropy","Heat Engines"],
      "Physics::Electrostatics":["Coulomb's Law","Electric Field","Gauss's Law","Potential & Energy","Capacitors","Dielectrics"],
      "Physics::Current Electricity":["Ohm's Law","Kirchhoff's Laws","Wheatstone Bridge","RC Circuits","Cell & EMF"],
      "Physics::Magnetism":["Biot-Savart Law","Ampere's Law","Magnetic Force","Moving Coil Galvanometer","Solenoid"],
      "Physics::EMI":["Faraday's Law","Lenz's Law","Self Inductance","Mutual Inductance","AC Circuits","Transformers"],
      "Physics::Optics":["Reflection","Refraction","Lens Formula","Total Internal Reflection","Interference","Diffraction"],
      "Physics::Modern Physics":["Photoelectric Effect","Bohr Model","de Broglie","Nuclear Reactions","Radioactivity","X-Rays"],
      "Physics::Waves":["Wave Equation","Superposition","Standing Waves","Doppler Effect","Resonance","Sound"],
      "Chemistry::Mole Concept":["Mole Definition","Avogadro's Number","Molar Mass","Stoichiometry","Limiting Reagent","% Composition"],
      "Chemistry::Atomic Structure":["Bohr Model","Quantum Numbers","Orbitals","Aufbau Principle","Electronic Configuration","Hund's Rule"],
      "Chemistry::Chemical Bonding":["Ionic Bonding","Covalent Bonding","VSEPR Theory","Hybridization","MO Theory","Hydrogen Bonding"],
      "Chemistry::Thermodynamics":["Enthalpy","Entropy","Gibbs Free Energy","Hess's Law","Bond Enthalpy","Kirchhoff's Equation"],
      "Chemistry::Equilibrium":["Kc & Kp","Le Chatelier's Principle","pH & Buffers","Solubility Product","Ionic Equilibrium"],
      "Chemistry::Electrochemistry":["Oxidation States","Galvanic Cell","Nernst Equation","Electrolysis","Kohlrausch's Law","Corrosion"],
      "Chemistry::Organic Basics":["IUPAC Naming","Isomerism","Inductive Effect","Resonance","Hyperconjugation","Reaction Types"],
      "Chemistry::Hydrocarbons":["Alkanes","Alkenes","Alkynes","Arenes","Markovnikov's Rule","Elimination vs Substitution"],
      "Chemistry::Aldehydes & Ketones":["Nucleophilic Addition","Aldol Condensation","Cannizzaro","Tollens Test","Benedict's Test"],
      "Chemistry::Coordination Chemistry":["Werner's Theory","Ligands & CFSE","Naming Complexes","Isomerism","EAN Rule"],
      "Chemistry::p-Block":["Group 13 (Boron)","Group 14 (Carbon)","Group 15 (Nitrogen)","Group 16 (Oxygen)","Group 17 (Halogens)","Group 18 (Noble)"],
      "Chemistry::d-Block":["Properties & Trends","Lanthanide Contraction","Complex Ions","Colour & Magnetism","Catalytic Activity"],
      "Maths::Limits & Continuity":["L'Hopital's Rule","Sandwich Theorem","Standard Limits","Continuity Conditions","Discontinuity Types"],
      "Maths::Differentiation":["Chain Rule","Product Rule","Quotient Rule","Implicit Diff.","Logarithmic Diff.","Higher Derivatives"],
      "Maths::Integration":["Substitution","By Parts","Partial Fractions","Definite Integrals","Properties of Definite","Reduction Formulae"],
      "Maths::Differential Equations":["Variable Separable","Homogeneous","Linear 1st Order","Exact Equations","Bernoulli Equation"],
      "Maths::Matrices":["Types of Matrices","Matrix Multiplication","Transpose","Inverse","Rank","System of Equations"],
      "Maths::Determinants":["Properties","Cofactor Expansion","Cramer's Rule","Adjoint","Area of Triangle"],
      "Maths::Vectors":["Dot Product","Cross Product","Triple Product","Projection","Direction Cosines"],
      "Maths::3D Geometry":["Direction Ratios","Line Equations","Plane Equations","Angle Between","Distance Formulae","Skew Lines"],
      "Maths::Probability":["Classical Probability","Conditional","Bayes Theorem","Binomial Distribution","Expectation"],
      "Maths::Complex Numbers":["Argand Plane","Modulus & Argument","De Moivre Theorem","Roots of Unity","Rotation"],
      "Maths::Conic Sections":["Circle","Parabola","Ellipse","Hyperbola","Parametric Forms","Tangent & Normal"],
      "Maths::Trigonometry":["Identities","Inverse Trig","Graphs","Solutions of Triangles","Height & Distance"],
    },
  },
  "NEET":{
    "name":"NEET UG","icon":"🩺","brand":"NEET","brandHL":"OS",
    "tagline":"Medical Entrance Preparation",
    "tiers":[[99,"🏆 AIIMS Rank"],[95,"⭐ Govt Medical"],[85,"✅ Top Private"],[0,"📈 Keep Pushing"]],
    "subjects":{
      "Physics":{"color":"#6366f1","icon":"⚛","topics":["Mechanics","Kinematics","Gravitation","Thermodynamics","Electrostatics","Current Electricity","Magnetism","Optics","Modern Physics","Waves","Fluid Mechanics","Units & Dimensions"]},
      "Chemistry":{"color":"#f97316","icon":"⬡","topics":["Atomic Structure","Chemical Bonding","Thermodynamics","Equilibrium","Electrochemistry","Organic Chemistry","Biomolecules","Polymers","Surface Chemistry","s-Block","p-Block","d-Block"]},
      "Biology":{"color":"#10b981","icon":"🧬","topics":["Cell Biology","Genetics","Evolution","Ecology","Human Physiology","Plant Physiology","Reproduction","Biotechnology","Animal Kingdom","Plant Kingdom","Biomolecules","Microbes"]},
    },
    "subtopics":{
      "Physics::Mechanics":["Newton's Laws","Work-Energy","Momentum","Friction","Circular Motion","Centre of Mass"],
      "Physics::Kinematics":["1D Motion","Projectile","Relative Motion","Motion Graphs"],
      "Physics::Gravitation":["Kepler's Laws","Gravitational Potential","Escape Velocity","Satellites"],
      "Physics::Thermodynamics":["First Law","PV Diagrams","Carnot Cycle","Kinetic Theory"],
      "Physics::Electrostatics":["Coulomb's Law","Electric Field","Gauss's Law","Capacitors"],
      "Physics::Current Electricity":["Ohm's Law","Kirchhoff's Laws","Wheatstone Bridge","RC Circuits"],
      "Physics::Magnetism":["Biot-Savart","Ampere's Law","Magnetic Force","Solenoid"],
      "Physics::Optics":["Reflection","Refraction","Lens Formula","Interference","Diffraction"],
      "Physics::Modern Physics":["Photoelectric Effect","Bohr Model","Radioactivity","Nuclear Fission"],
      "Physics::Waves":["Wave Equation","Standing Waves","Doppler Effect","Sound Waves"],
      "Physics::Fluid Mechanics":["Bernoulli's Theorem","Viscosity","Surface Tension","Pascal's Law"],
      "Physics::Units & Dimensions":["SI Units","Dimensional Analysis","Error Analysis","Significant Figures"],
      "Chemistry::Atomic Structure":["Bohr Model","Quantum Numbers","Orbitals","Electronic Configuration"],
      "Chemistry::Chemical Bonding":["Ionic Bond","Covalent Bond","VSEPR","Hybridization","Hydrogen Bond"],
      "Chemistry::Thermodynamics":["Enthalpy","Entropy","Gibbs Energy","Hess's Law"],
      "Chemistry::Equilibrium":["Kc & Kp","Le Chatelier","pH & Buffers","Solubility Product"],
      "Chemistry::Electrochemistry":["Galvanic Cell","Nernst Equation","Electrolysis","Corrosion"],
      "Chemistry::Organic Chemistry":["IUPAC Naming","Isomerism","Reaction Mechanisms","Functional Groups","Aldehydes & Ketones"],
      "Chemistry::Biomolecules":["Carbohydrates","Proteins","Lipids","Nucleic Acids","Enzymes"],
      "Chemistry::Polymers":["Types","Addition Polymers","Condensation Polymers","Biodegradable"],
      "Chemistry::Surface Chemistry":["Adsorption","Catalysis","Colloids","Emulsions"],
      "Chemistry::s-Block":["Group 1 (Alkali)","Group 2 (Alkaline Earth)","Compounds","Anomalous Properties"],
      "Chemistry::p-Block":["Group 13-18","Halides","Oxides","Oxyacids"],
      "Chemistry::d-Block":["Transition Metals","Properties","Complex Ions","Lanthanides"],
      "Biology::Cell Biology":["Cell Structure","Cell Organelles","Cell Division","Cell Cycle","Membrane Transport"],
      "Biology::Genetics":["Mendelian Genetics","Chromosomal Theory","DNA Replication","Gene Expression","Genetic Disorders"],
      "Biology::Evolution":["Origin of Life","Natural Selection","Adaptive Radiation","Human Evolution"],
      "Biology::Ecology":["Ecosystems","Biodiversity","Environmental Issues","Population Ecology"],
      "Biology::Human Physiology":["Digestion","Respiration","Circulation","Excretion","Neural Control","Endocrine System"],
      "Biology::Plant Physiology":["Photosynthesis","Respiration","Mineral Nutrition","Transport in Plants","Growth"],
      "Biology::Reproduction":["Human Reproduction","Plant Reproduction","Reproductive Health","Embryology"],
      "Biology::Biotechnology":["rDNA Technology","PCR","Gene Therapy","Transgenic Organisms","Bioethics"],
      "Biology::Animal Kingdom":["Classification","Phyla","Structural Organization","Body Plans"],
      "Biology::Plant Kingdom":["Algae","Bryophytes","Pteridophytes","Gymnosperms","Angiosperms"],
      "Biology::Biomolecules":["Carbohydrates","Proteins","Lipids","Nucleic Acids","Enzymes"],
      "Biology::Microbes":["Bacteria","Viruses","Fungi","Protozoa","Microbes in Industry"],
    },
  },
  "UPSC":{
    "name":"UPSC Civil Services","icon":"🏛️","brand":"UPSC","brandHL":"OS",
    "tagline":"IAS / IPS / IFS Preparation",
    "tiers":[[99,"🏆 Top 50 IAS"],[95,"⭐ CSE Qualified"],[85,"✅ Prelims Clear"],[0,"📈 Keep Pushing"]],
    "subjects":{
      "History":{"color":"#f59e0b","icon":"📜","topics":["Ancient India","Medieval India","Modern India","World History","Art & Culture","Freedom Movement","Post-Independence"]},
      "Geography":{"color":"#10b981","icon":"🌍","topics":["Physical Geography","Indian Geography","World Geography","Climatology","Oceanography","Environment","Mapping"]},
      "Polity":{"color":"#6366f1","icon":"⚖️","topics":["Constitution","Fundamental Rights","Parliament","Judiciary","State Government","Local Government","Amendments"]},
      "Economy":{"color":"#f97316","icon":"📊","topics":["Microeconomics","Macroeconomics","Indian Economy","Budget & Fiscal","Banking & Finance","International Trade","Economic Reforms"]},
      "Science":{"color":"#8b5cf6","icon":"🔬","topics":["Physics Basics","Chemistry Basics","Biology Basics","Space & Technology","Health & Medicine","Environment & Ecology","IT & Computers"]},
      "Ethics":{"color":"#ec4899","icon":"🧭","topics":["Ethics Theory","Attitude","Aptitude","Emotional Intelligence","Public Administration","Probity","Case Studies"]},
    },
    "subtopics":{
      "History::Ancient India":["Indus Valley","Vedic Period","Mauryan Empire","Gupta Empire","Buddhism & Jainism"],
      "History::Medieval India":["Delhi Sultanate","Mughal Empire","Bhakti Movement","Vijayanagara","Maratha Empire"],
      "History::Modern India":["British Rule","Revolt of 1857","Social Reforms","Gandhi Era","Partition"],
      "History::World History":["Industrial Revolution","World Wars","Cold War","Decolonization","Globalization"],
      "History::Art & Culture":["Architecture","Painting","Dance & Music","Literature","UNESCO Sites"],
      "History::Freedom Movement":["Early Nationalism","Extremist Phase","Non-Cooperation","Quit India","INA"],
      "History::Post-Independence":["Integration of States","Five Year Plans","Green Revolution","Emergency","Liberalization"],
      "Geography::Physical Geography":["Geomorphology","Atmosphere","Hydrosphere","Biogeography","Tectonics"],
      "Geography::Indian Geography":["Physiography","Rivers","Climate","Soils","Natural Vegetation"],
      "Geography::World Geography":["Continents","Oceans","Major Cities","Resource Distribution"],
      "Geography::Climatology":["Weather Systems","Monsoons","El Nino","Climate Change"],
      "Geography::Oceanography":["Ocean Currents","Tides","Marine Resources","Coral Reefs"],
      "Geography::Environment":["Biodiversity","Pollution","Conservation","Sustainable Development"],
      "Geography::Mapping":["Map Reading","GIS","Remote Sensing","Cartography"],
      "Polity::Constitution":["Preamble","Features","Schedules","Historical Background"],
      "Polity::Fundamental Rights":["Articles 12-35","Right to Equality","Freedom of Speech","Writs"],
      "Polity::Parliament":["Lok Sabha","Rajya Sabha","Legislative Process","Parliamentary Committees"],
      "Polity::Judiciary":["Supreme Court","High Courts","Judicial Review","PIL"],
      "Polity::State Government":["Governor","CM & Council","State Legislature","Centre-State Relations"],
      "Polity::Local Government":["Panchayati Raj","Municipalities","73rd & 74th Amendments","Finance Commission"],
      "Polity::Amendments":["Key Amendments","Amendment Process","Basic Structure Doctrine","Landmark Cases"],
      "Economy::Microeconomics":["Demand & Supply","Elasticity","Market Structures","Consumer Theory"],
      "Economy::Macroeconomics":["GDP","Inflation","Unemployment","Monetary Policy","Fiscal Policy"],
      "Economy::Indian Economy":["Agriculture","Industry","Services","Poverty","Inequality"],
      "Economy::Budget & Fiscal":["Union Budget","FRBM Act","GST","Tax Structure"],
      "Economy::Banking & Finance":["RBI","Commercial Banks","NBFC","Stock Markets","Insurance"],
      "Economy::International Trade":["WTO","Balance of Payments","FDI","Exchange Rates"],
      "Economy::Economic Reforms":["LPG Reforms","Make in India","PLI Scheme","Digital Economy"],
      "Science::Physics Basics":["Motion","Force","Energy","Heat","Light","Electricity"],
      "Science::Chemistry Basics":["Atoms","Chemical Reactions","Acids & Bases","Metals","Organic"],
      "Science::Biology Basics":["Cell","Genetics","Evolution","Human Body","Diseases"],
      "Science::Space & Technology":["ISRO","Satellites","Space Missions","Nuclear Technology"],
      "Science::Health & Medicine":["Diseases","Vaccines","Nutrition","Public Health","Biotechnology"],
      "Science::Environment & Ecology":["Ecosystems","Climate Change","Wildlife","Pollution","Treaties"],
      "Science::IT & Computers":["Artificial Intelligence","Blockchain","Cyber Security","IoT"],
      "Ethics::Ethics Theory":["Thinkers","Moral Philosophy","Applied Ethics","Deontology","Virtue Ethics"],
      "Ethics::Attitude":["Content","Structure","Functions","Influence","Moral Attitude"],
      "Ethics::Aptitude":["Foundational Values","Integrity","Impartiality","Objectivity"],
      "Ethics::Emotional Intelligence":["Concepts","Components","Utility","Applications"],
      "Ethics::Public Administration":["Governance","Accountability","Transparency","RTI"],
      "Ethics::Probity":["Concept","Codes of Conduct","Corruption","Work Culture"],
      "Ethics::Case Studies":["Framework","Stakeholder Analysis","Ethical Dilemmas","Decision Making"],
    },
  },
  "CAT":{
    "name":"CAT (MBA Entrance)","icon":"📈","brand":"CAT","brandHL":"OS",
    "tagline":"IIM / Top B-School Preparation",
    "tiers":[[99,"🏆 IIM A/B/C Call"],[95,"⭐ Top IIM Zone"],[85,"✅ IIM Shortlist"],[0,"📈 Keep Pushing"]],
    "subjects":{
      "Quant":{"color":"#6366f1","icon":"🔢","topics":["Arithmetic","Algebra","Number System","Geometry","Mensuration","Modern Math","Trigonometry"]},
      "VARC":{"color":"#f97316","icon":"📖","topics":["Reading Comprehension","Para Jumbles","Para Summary","Sentence Completion","Critical Reasoning","Vocab-Based","Odd Sentence"]},
      "DILR":{"color":"#8b5cf6","icon":"🧩","topics":["Data Interpretation","Logical Reasoning","Puzzles & Arrangements","Data Sufficiency","Caselets","Games & Tournaments","Networks"]},
    },
    "subtopics":{
      "Quant::Arithmetic":["Percentages","Profit & Loss","SI/CI","Ratio & Proportion","Time & Work","Time-Speed-Distance","Averages & Mixtures"],
      "Quant::Algebra":["Linear Equations","Quadratics","Inequalities","Functions","Logarithms","Progressions"],
      "Quant::Number System":["Divisibility","Remainders","Factors","HCF & LCM","Base System"],
      "Quant::Geometry":["Triangles","Circles","Quadrilaterals","Coordinate Geometry","Similarity"],
      "Quant::Mensuration":["Area","Volume","Surface Area","Solids"],
      "Quant::Modern Math":["Permutations","Combinations","Probability","Set Theory"],
      "Quant::Trigonometry":["Ratios","Identities","Heights & Distances"],
      "VARC::Reading Comprehension":["Science Passages","Philosophy","Economics","Literature","Social Issues"],
      "VARC::Para Jumbles":["4-Sentence","5-Sentence","Odd One Out"],
      "VARC::Para Summary":["Main Idea","Inference","Summary Sentence"],
      "VARC::Sentence Completion":["Grammar-Based","Vocab-Based","Logic-Based"],
      "VARC::Critical Reasoning":["Strengthen","Weaken","Assumption","Conclusion"],
      "VARC::Vocab-Based":["Analogies","Fill in Blanks","Word Usage"],
      "VARC::Odd Sentence":["Theme Detection","Logical Flow","Elimination"],
      "DILR::Data Interpretation":["Bar Graphs","Pie Charts","Tables","Line Graphs","Mixed Sets"],
      "DILR::Logical Reasoning":["Blood Relations","Direction","Coding","Syllogisms"],
      "DILR::Puzzles & Arrangements":["Linear","Circular","Matrix","Scheduling"],
      "DILR::Data Sufficiency":["Quantitative DS","Logical DS"],
      "DILR::Caselets":["Paragraph-Based DI","Multi-Table","Calculation Heavy"],
      "DILR::Games & Tournaments":["Knockout","Round Robin","Rankings"],
      "DILR::Networks":["Routing","Flow Charts","Connections"],
    },
  },
  "GATE":{
    "name":"GATE (CS/IT)","icon":"💻","brand":"GATE","brandHL":"OS",
    "tagline":"M.Tech / PSU Entrance Preparation",
    "tiers":[[99,"🏆 IIT M.Tech"],[95,"⭐ NIT M.Tech"],[85,"✅ PSU Eligible"],[0,"📈 Keep Pushing"]],
    "subjects":{
      "DSA":{"color":"#6366f1","icon":"🌲","topics":["Arrays","Linked Lists","Stacks & Queues","Trees","Graphs","Hashing","Heaps","Sorting","Searching","Dynamic Programming"]},
      "OS":{"color":"#f97316","icon":"⚙️","topics":["Process Management","CPU Scheduling","Synchronization","Deadlocks","Memory Management","Virtual Memory","File Systems","I/O Systems"]},
      "DBMS":{"color":"#10b981","icon":"🗄️","topics":["ER Model","Relational Model","SQL","Normalization","Transactions","Concurrency","Indexing","File Organization"]},
      "Networks":{"color":"#8b5cf6","icon":"🌐","topics":["OSI Model","TCP/IP","Data Link Layer","Network Layer","Transport Layer","Application Layer","Security","Wireless"]},
      "TOC":{"color":"#ec4899","icon":"🔄","topics":["Finite Automata","Regular Languages","Context-Free Grammar","Pushdown Automata","Turing Machines","Decidability","Complexity"]},
    },
    "subtopics":{
      "DSA::Arrays":["1D/2D Arrays","Searching","Sorting","Matrix Operations"],
      "DSA::Linked Lists":["Singly","Doubly","Circular","Operations"],
      "DSA::Stacks & Queues":["Implementation","Applications","Priority Queue","Deque"],
      "DSA::Trees":["Binary Tree","BST","AVL","B-Tree","Traversals"],
      "DSA::Graphs":["BFS","DFS","Shortest Path","MST","Topological Sort"],
      "DSA::Hashing":["Hash Functions","Collision Resolution","Open Addressing","Chaining"],
      "DSA::Heaps":["Min/Max Heap","Heap Sort","Priority Queue","Binomial Heap"],
      "DSA::Sorting":["Bubble","Merge","Quick","Heap","Radix","Counting"],
      "DSA::Searching":["Linear","Binary","Interpolation","Hashing"],
      "DSA::Dynamic Programming":["Memoization","Tabulation","LCS","Knapsack","Matrix Chain"],
      "OS::Process Management":["Process States","PCB","Fork","IPC","Threads"],
      "OS::CPU Scheduling":["FCFS","SJF","Round Robin","Priority","Multilevel"],
      "OS::Synchronization":["Critical Section","Semaphores","Monitors","Mutex"],
      "OS::Deadlocks":["Conditions","Prevention","Avoidance","Detection","Banker's Algorithm"],
      "OS::Memory Management":["Paging","Segmentation","Allocation","Fragmentation"],
      "OS::Virtual Memory":["Page Replacement","Thrashing","TLB","Demand Paging"],
      "OS::File Systems":["Directory Structure","Allocation Methods","Free Space","Protection"],
      "OS::I/O Systems":["Device Drivers","Buffering","Spooling","RAID"],
      "DBMS::ER Model":["Entities","Relationships","Attributes","Cardinality","Participation"],
      "DBMS::Relational Model":["Keys","Relational Algebra","Relational Calculus","Constraints"],
      "DBMS::SQL":["DDL","DML","Joins","Subqueries","Views","Triggers"],
      "DBMS::Normalization":["1NF","2NF","3NF","BCNF","4NF","5NF"],
      "DBMS::Transactions":["ACID","Serializability","Recovery","Logging"],
      "DBMS::Concurrency":["Lock-Based","Timestamp","MVCC","Deadlock Handling"],
      "DBMS::Indexing":["B-Tree","B+ Tree","Hash Index","Bitmap"],
      "DBMS::File Organization":["Sequential","Indexed","Hashed","Clustered"],
      "Networks::OSI Model":["Layers","Functions","Protocols","Comparison with TCP/IP"],
      "Networks::TCP/IP":["IP Addressing","Subnetting","IPv6","ARP","ICMP"],
      "Networks::Data Link Layer":["Framing","Error Detection","Flow Control","MAC"],
      "Networks::Network Layer":["Routing Algorithms","OSPF","BGP","IP Fragmentation"],
      "Networks::Transport Layer":["TCP","UDP","Congestion Control","Flow Control"],
      "Networks::Application Layer":["HTTP","DNS","SMTP","FTP","DHCP"],
      "Networks::Security":["Encryption","Firewall","SSL/TLS","VPN","Authentication"],
      "Networks::Wireless":["WiFi","Bluetooth","Cellular","Ad-hoc Networks"],
      "TOC::Finite Automata":["DFA","NFA","NFA to DFA","Minimization"],
      "TOC::Regular Languages":["Regular Expressions","Pumping Lemma","Closure Properties"],
      "TOC::Context-Free Grammar":["Parse Trees","Ambiguity","CNF","GNF"],
      "TOC::Pushdown Automata":["DPDA","NPDA","CFG to PDA","Acceptance"],
      "TOC::Turing Machines":["Definition","Variants","Church-Turing Thesis"],
      "TOC::Decidability":["Halting Problem","Rice's Theorem","Reduction","Undecidable Languages"],
      "TOC::Complexity":["P vs NP","NP-Complete","NP-Hard","Reductions"],
    },
  },
  "CLAT":{
    "name":"CLAT (Law Entrance)","icon":"⚖️","brand":"CLAT","brandHL":"OS",
    "tagline":"NLU / Top Law School Preparation",
    "tiers":[[99,"🏆 NLSIU Rank"],[95,"⭐ Top 5 NLU"],[85,"✅ NLU Qualified"],[0,"📈 Keep Pushing"]],
    "subjects":{
      "English":{"color":"#6366f1","icon":"📝","topics":["Reading Comprehension","Grammar","Vocabulary","Para Jumbles","Error Correction","Sentence Improvement","Cloze Test"]},
      "Legal Reasoning":{"color":"#f97316","icon":"⚖️","topics":["Legal Principles","Legal Maxims","Constitutional Law","Criminal Law","Contract Law","Tort Law","Current Legal Affairs"]},
      "Logical Reasoning":{"color":"#8b5cf6","icon":"🧠","topics":["Analogies","Series Completion","Syllogisms","Critical Reasoning","Assumptions","Strengthening & Weakening","Statement & Conclusion"]},
      "GK":{"color":"#10b981","icon":"🌐","topics":["Indian History","World History","Indian Polity","Geography","Science","Economy","Current Affairs"]},
      "Maths":{"color":"#ec4899","icon":"🔢","topics":["Arithmetic","Algebra","Data Interpretation","Mensuration","Statistics","Number System","Ratio & Proportion"]},
    },
    "subtopics":{
      "English::Reading Comprehension":["Factual","Inferential","Vocabulary in Context","Tone","Main Idea"],
      "English::Grammar":["Tenses","Subject-Verb Agreement","Articles","Prepositions"],
      "English::Vocabulary":["Synonyms","Antonyms","Idioms","One-Word Substitution"],
      "English::Para Jumbles":["Sentence Ordering","Logical Flow","Connectors"],
      "English::Error Correction":["Grammatical Errors","Spelling","Punctuation"],
      "English::Sentence Improvement":["Rephrasing","Clarity","Conciseness"],
      "English::Cloze Test":["Context Clues","Grammar-Based","Vocabulary-Based"],
      "Legal Reasoning::Legal Principles":["Application","Fact Pattern","Ratio Decidendi"],
      "Legal Reasoning::Legal Maxims":["Latin Maxims","Application","Exceptions"],
      "Legal Reasoning::Constitutional Law":["Fundamental Rights","DPSP","Amendments"],
      "Legal Reasoning::Criminal Law":["IPC Basics","Mens Rea","Actus Reus","Defences"],
      "Legal Reasoning::Contract Law":["Offer & Acceptance","Consideration","Breach"],
      "Legal Reasoning::Tort Law":["Negligence","Strict Liability","Defamation"],
      "Legal Reasoning::Current Legal Affairs":["Recent Judgments","New Legislation","Legal News"],
      "Logical Reasoning::Analogies":["Verbal","Number","Letter"],
      "Logical Reasoning::Series Completion":["Number","Letter","Pattern"],
      "Logical Reasoning::Syllogisms":["Two Premises","Three Premises","Negative"],
      "Logical Reasoning::Critical Reasoning":["Arguments","Counter-Arguments","Fallacies"],
      "Logical Reasoning::Assumptions":["Implicit","Explicit","Underlying"],
      "Logical Reasoning::Strengthening & Weakening":["Evidence","Counter-Evidence"],
      "Logical Reasoning::Statement & Conclusion":["Validity","Logical Deduction"],
      "GK::Indian History":["Ancient","Medieval","Modern","Freedom Struggle"],
      "GK::World History":["Ancient Civilizations","World Wars","Cold War","Modern"],
      "GK::Indian Polity":["Constitution","Parliament","Judiciary","Governance"],
      "GK::Geography":["Indian Geography","World Geography","Climate","Resources"],
      "GK::Science":["Physics","Chemistry","Biology","Space & Technology"],
      "GK::Economy":["Indian Economy","Banking","Budget","International"],
      "GK::Current Affairs":["National","International","Sports","Awards"],
      "Maths::Arithmetic":["Percentage","Profit & Loss","SI/CI","Averages"],
      "Maths::Algebra":["Equations","Inequalities","Progressions"],
      "Maths::Data Interpretation":["Bar Graphs","Pie Charts","Tables"],
      "Maths::Mensuration":["Area","Volume","Perimeter"],
      "Maths::Statistics":["Mean","Median","Mode","Standard Deviation"],
      "Maths::Number System":["Divisibility","HCF & LCM","Prime Numbers"],
      "Maths::Ratio & Proportion":["Direct","Inverse","Partnership"],
    },
  },
  "SSC":{
    "name":"SSC CGL","icon":"🏢","brand":"SSC","brandHL":"OS",
    "tagline":"Government Job Preparation",
    "tiers":[[99,"🏆 Top Selection"],[95,"⭐ Interview Zone"],[85,"✅ Prelims Clear"],[0,"📈 Keep Pushing"]],
    "subjects":{
      "Quant":{"color":"#6366f1","icon":"🔢","topics":["Arithmetic","Algebra","Geometry","Trigonometry","Mensuration","Data Interpretation","Number System"]},
      "English":{"color":"#f97316","icon":"📖","topics":["Reading Comprehension","Grammar","Vocabulary","Error Detection","Sentence Improvement","Cloze Test","Idioms & Phrases"]},
      "Reasoning":{"color":"#8b5cf6","icon":"🧠","topics":["Coding-Decoding","Series","Analogies","Classification","Blood Relations","Direction","Venn Diagrams"]},
      "GK":{"color":"#10b981","icon":"🌐","topics":["History","Geography","Polity","Economy","Science","Current Affairs","Static GK"]},
    },
    "subtopics":{
      "Quant::Arithmetic":["Percentage","Profit & Loss","SI/CI","Time & Work","Speed & Distance","Averages","Mixtures"],
      "Quant::Algebra":["Linear Equations","Quadratics","Surds & Indices","Algebraic Identities"],
      "Quant::Geometry":["Triangles","Circles","Quadrilaterals","Coordinate Geometry"],
      "Quant::Trigonometry":["Ratios","Identities","Heights & Distances"],
      "Quant::Mensuration":["Area","Volume","Surface Area"],
      "Quant::Data Interpretation":["Bar","Pie","Line","Table","Mixed"],
      "Quant::Number System":["Divisibility","Factors","Remainders","HCF & LCM"],
      "English::Reading Comprehension":["Factual","Inferential","Vocabulary"],
      "English::Grammar":["Tenses","Active-Passive","Direct-Indirect","Articles"],
      "English::Vocabulary":["Synonyms","Antonyms","One-Word Substitution"],
      "English::Error Detection":["Subject-Verb","Tense","Preposition","Article"],
      "English::Sentence Improvement":["Rephrasing","Clarity","Idiomatic"],
      "English::Cloze Test":["Context","Grammar","Vocabulary"],
      "English::Idioms & Phrases":["Common Idioms","Proverbs","Phrasal Verbs"],
      "Reasoning::Coding-Decoding":["Letter","Number","Mixed"],
      "Reasoning::Series":["Number","Letter","Alpha-Numeric"],
      "Reasoning::Analogies":["Verbal","Number","Letter"],
      "Reasoning::Classification":["Odd One Out","Grouping"],
      "Reasoning::Blood Relations":["Family Tree","Coded Relations"],
      "Reasoning::Direction":["Distance","Turns","Shadow"],
      "Reasoning::Venn Diagrams":["Two Sets","Three Sets","Logical"],
      "GK::History":["Ancient","Medieval","Modern","Freedom Struggle"],
      "GK::Geography":["Indian","Physical","Climate","Rivers"],
      "GK::Polity":["Constitution","Parliament","Judiciary","Governance"],
      "GK::Economy":["Banking","Budget","Taxation","Schemes"],
      "GK::Science":["Physics","Chemistry","Biology","Technology"],
      "GK::Current Affairs":["National","International","Sports","Awards"],
      "GK::Static GK":["National Parks","Dams","Capitals","Organizations"],
    },
  },
  "Banking":{
    "name":"Banking (IBPS/SBI)","icon":"🏦","brand":"Bank","brandHL":"OS",
    "tagline":"Bank PO / Clerk Preparation",
    "tiers":[[99,"🏆 PO Selected"],[95,"⭐ Interview Zone"],[85,"✅ Prelims Clear"],[0,"📈 Keep Pushing"]],
    "subjects":{
      "Quant":{"color":"#6366f1","icon":"🔢","topics":["Number Series","Simplification","Data Interpretation","Arithmetic","Quadratic Equations","Data Sufficiency","Miscellaneous"]},
      "English":{"color":"#f97316","icon":"📖","topics":["Reading Comprehension","Cloze Test","Error Detection","Sentence Rearrangement","Fill in Blanks","Column Based","Vocabulary"]},
      "Reasoning":{"color":"#8b5cf6","icon":"🧠","topics":["Puzzles","Seating Arrangement","Syllogism","Coding-Decoding","Blood Relations","Inequality","Data Sufficiency"]},
      "GK":{"color":"#10b981","icon":"🌐","topics":["Banking Awareness","Financial Awareness","Current Affairs","Static GK","Economy","Government Schemes","RBI & SEBI"]},
      "Computer":{"color":"#ec4899","icon":"💻","topics":["Hardware Basics","Software Basics","Networking","MS Office","Internet","Cyber Security","Database Basics"]},
    },
    "subtopics":{
      "Quant::Number Series":["Missing Number","Wrong Number","Pattern Recognition"],
      "Quant::Simplification":["BODMAS","Approximation","Surds"],
      "Quant::Data Interpretation":["Bar Graph","Pie Chart","Line Graph","Table","Caselet"],
      "Quant::Arithmetic":["Percentage","Profit & Loss","SI/CI","Time & Work","Speed & Distance","Averages","Ratio"],
      "Quant::Quadratic Equations":["Roots","Factoring","Comparison"],
      "Quant::Data Sufficiency":["Quantitative","Two Statements","Three Statements"],
      "Quant::Miscellaneous":["Probability","Permutation","Boats & Streams","Pipes & Cisterns"],
      "English::Reading Comprehension":["Banking Passages","Economy Passages","Social Issues"],
      "English::Cloze Test":["Single Blank","Double Blank","New Pattern"],
      "English::Error Detection":["Grammar","Spelling","Sentence Correction"],
      "English::Sentence Rearrangement":["Para Jumbles","Sentence Ordering"],
      "English::Fill in Blanks":["Single","Double","Phrasal"],
      "English::Column Based":["Match Columns","Connector Based"],
      "English::Vocabulary":["Synonyms","Antonyms","Idioms","Phrases"],
      "Reasoning::Puzzles":["Floor Based","Box Based","Month Based","Day Based"],
      "Reasoning::Seating Arrangement":["Linear","Circular","Square","Rectangular"],
      "Reasoning::Syllogism":["Two Premises","Possibility","Negative"],
      "Reasoning::Coding-Decoding":["Letter","Number","Condition Based"],
      "Reasoning::Blood Relations":["Family Tree","Coded","Pointing"],
      "Reasoning::Inequality":["Coded","Direct","Chain"],
      "Reasoning::Data Sufficiency":["Two Statements","Three Statements"],
      "GK::Banking Awareness":["Types of Banks","Banking Terms","NPA","Basel Norms"],
      "GK::Financial Awareness":["Stock Market","Mutual Funds","Insurance","Fintech"],
      "GK::Current Affairs":["National","International","Banking News","Appointments"],
      "GK::Static GK":["Headquarters","Taglines","Founders","Capitals"],
      "GK::Economy":["GDP","Inflation","Fiscal Policy","Monetary Policy"],
      "GK::Government Schemes":["PM Schemes","Financial Inclusion","Digital India"],
      "GK::RBI & SEBI":["Functions","Policies","Rates","Regulations"],
      "Computer::Hardware Basics":["CPU","Memory","I/O Devices","Storage"],
      "Computer::Software Basics":["OS","Application Software","Languages"],
      "Computer::Networking":["LAN/WAN","Protocols","Internet","Cloud"],
      "Computer::MS Office":["Word","Excel","PowerPoint","Shortcuts"],
      "Computer::Internet":["Browsers","Email","WWW","Search Engines"],
      "Computer::Cyber Security":["Viruses","Firewall","Encryption","Phishing"],
      "Computer::Database Basics":["DBMS Concepts","SQL Basics","Keys","Normalization"],
    },
  },
}

def get_exam(exam_type):
    return EXAMS.get(exam_type, EXAMS["JEE"])

EXAM_LIST = list(EXAMS.keys())

QUOTES = [
    "Every topper was once exactly where you are right now.",
    "Your past doesn't define your rank. Only your next two hours matter.",
    "The pain you feel today is the strength you'll feel at result day.",
    "Consistency beats brilliance. It always has. It always will.",
    "You didn't come this far to give up now. Never.",
    "One more hour today means one rank higher tomorrow.",
    "Top 0.1% is not luck — it's 10,000 hours of focused work.",
]
CHANGELOG = [
    ("v3.0","Multi-Exam Support","Choose from JEE, NEET, UPSC, CAT, GATE, CLAT, SSC, Banking — all customized."),
    ("v2.0","Multi-user login system","Create your account, log in securely, and keep all your data private."),
    ("v2.0","Custom Priority Queue","Set your own study priorities or let AI pick based on your weak areas."),
    ("v2.0","Friends & Leaderboard","Add friends by username and compete on percentile, hours, and mastery."),
    ("v2.0","Doubts Community","Post doubts with images. Reply to classmates. Mark solutions."),
    ("v2.0","PDF Report Generator","Download a professional performance report with charts and analytics."),
    ("v2.0","Activity Log","Track every action — tests added, hours logged, doubts posted."),
]

def calc_pct(*scores):
    vals=[s for s in scores if s is not None]
    if not vals: return 0
    n=sum(vals)/len(vals)
    if n>=90: return round(99+(n-90)*0.1,2)
    if n>=80: return round(95+(n-80)*0.4,2)
    if n>=70: return round(88+(n-70)*0.7,2)
    if n>=60: return round(78+(n-60)*1.0,2)
    if n>=50: return round(60+(n-50)*1.8,2)
    return round(max(10,n*1.2),2)

def get_streak(log):
    s,today=0,datetime.date.today()
    for i in range(30):
        k=(today-datetime.timedelta(days=i)).isoformat()
        if log.get(k,0)>0: s+=1
        else: break
    return s

def weak_topics(scores,n=8):
    out=[]
    for k,v in sorted(scores.items(),key=lambda x:x[1]):
        if '::' in k:
            sub,top=k.split('::',1)
            out.append({"key":k,"subject":sub,"topic":top,"score":v})
    return out[:n]

def gen_plan(scores,priority=None):
    items = [{"key":k,"subject":k.split('::')[0],"topic":k.split('::')[1],"score":scores.get(k,0)} for k in priority if '::' in k] if priority else weak_topics(scores,6)
    plan,rem=[],8.0
    for i,item in enumerate(items[:6]):
        h=1.5 if item["score"]<40 else(1.0 if item["score"]<60 else 0.75)
        if rem>0:
            a=min(h,rem); plan.append({**item,"hours":round(a,2),"time":f"{9+i}:00"}); rem-=a
    return plan

# ═══════════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════════
def db():
    c=sqlite3.connect(DB,check_same_thread=False,timeout=30)
    c.row_factory=sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("PRAGMA busy_timeout=5000")
    return c

def init_db():
    c=sqlite3.connect(DB,check_same_thread=False,timeout=30)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    c.close()
    c=db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        pw_hash TEXT NOT NULL, pw_salt TEXT NOT NULL,
        name TEXT DEFAULT '', avatar TEXT DEFAULT '🎯',
        bio TEXT DEFAULT '', college TEXT DEFAULT '',
        exam_type TEXT DEFAULT 'JEE',
        exam_date TEXT DEFAULT '', theme TEXT DEFAULT 'dark',
        created_at TEXT DEFAULT(datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS sessions(
        token TEXT PRIMARY KEY, user_id INTEGER NOT NULL,
        expires_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS topic_scores(
        user_id INTEGER NOT NULL, key TEXT NOT NULL, score REAL DEFAULT 0,
        PRIMARY KEY(user_id,key),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS checked(
        user_id INTEGER NOT NULL, key TEXT NOT NULL, val INTEGER DEFAULT 0,
        PRIMARY KEY(user_id,key),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS mock_tests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL, date TEXT NOT NULL,
        physics REAL, chemistry REAL, maths REAL,
        scores_json TEXT DEFAULT '{}',
        percentile REAL, notes TEXT DEFAULT '',
        created_at TEXT DEFAULT(datetime('now')),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS study_log(
        user_id INTEGER NOT NULL, date TEXT NOT NULL, hours REAL DEFAULT 0,
        PRIMARY KEY(user_id,date),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS priority(
        user_id INTEGER NOT NULL, key TEXT NOT NULL, pos INTEGER DEFAULT 0,
        PRIMARY KEY(user_id,key),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS friends(
        user_id INTEGER NOT NULL, friend_id INTEGER NOT NULL, status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT(datetime('now')),
        PRIMARY KEY(user_id,friend_id),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(friend_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS doubts(
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
        title TEXT NOT NULL, body TEXT NOT NULL, subject TEXT DEFAULT 'General',
        media_type TEXT DEFAULT 'none', media_b64 TEXT DEFAULT '',
        solved INTEGER DEFAULT 0,
        created_at TEXT DEFAULT(datetime('now')), updated_at TEXT DEFAULT(datetime('now')),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS replies(
        id INTEGER PRIMARY KEY AUTOINCREMENT, doubt_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL, body TEXT NOT NULL,
        created_at TEXT DEFAULT(datetime('now')), updated_at TEXT DEFAULT(datetime('now')),
        FOREIGN KEY(doubt_id) REFERENCES doubts(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS activity(
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
        action TEXT NOT NULL, detail TEXT DEFAULT '',
        created_at TEXT DEFAULT(datetime('now')),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    c.commit()
    # Migrate existing databases
    try: c.execute("ALTER TABLE users ADD COLUMN exam_type TEXT DEFAULT 'JEE'")
    except: pass
    try: c.execute("ALTER TABLE mock_tests ADD COLUMN scores_json TEXT DEFAULT '{}'")
    except: pass
    c.commit(); c.close()
    print("✅ Database ready")

def hp(pw,salt=None):
    if not salt: salt=secrets.token_hex(16)
    h=hashlib.pbkdf2_hmac("sha256",pw.encode(),salt.encode(),260000).hex()
    return salt,h

def make_token(uid):
    t=secrets.token_urlsafe(32)
    exp=(datetime.datetime.now()+datetime.timedelta(days=30)).isoformat()
    c=db()
    try:
        c.execute("INSERT INTO sessions(token,user_id,expires_at) VALUES(?,?,?)",(t,uid,exp))
        c.commit()
    finally:
        c.close()
    return t

def user_from_token(tok):
    if not tok: return None
    c=db()
    try:
        r=c.execute("SELECT u.* FROM users u JOIN sessions s ON s.user_id=u.id WHERE s.token=? AND s.expires_at>datetime('now')",(tok,)).fetchone()
        return dict(r) if r else None
    finally:
        c.close()

def log_act(uid,action,detail=""):
    c=db()
    try:
        c.execute("INSERT INTO activity(user_id,action,detail) VALUES(?,?,?)",(uid,action,detail)); c.commit()
    finally:
        c.close()

def get_user_data(uid):
    c=db()
    try:
        scores={r["key"]:r["score"] for r in c.execute("SELECT key,score FROM topic_scores WHERE user_id=?",(uid,)).fetchall()}
        chk={r["key"]:bool(r["val"]) for r in c.execute("SELECT key,val FROM checked WHERE user_id=?",(uid,)).fetchall()}
        tests=[dict(r) for r in c.execute("SELECT * FROM mock_tests WHERE user_id=? ORDER BY date,id",(uid,)).fetchall()]
        log={r["date"]:r["hours"] for r in c.execute("SELECT date,hours FROM study_log WHERE user_id=?",(uid,)).fetchall()}
        prio=[r["key"] for r in c.execute("SELECT key FROM priority WHERE user_id=? ORDER BY pos",(uid,)).fetchall()]
        acts=[dict(r) for r in c.execute("SELECT action,detail,created_at FROM activity WHERE user_id=? ORDER BY id DESC LIMIT 50",(uid,)).fetchall()]
        return {"scores":scores,"checked":chk,"tests":tests,"log":log,"priority":prio,"activity":acts}
    finally:
        c.close()

# ═══════════════════════════════════════════════════════════════════════
# PDF REPORT
# ═══════════════════════════════════════════════════════════════════════
def make_pdf(user,data):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor,white
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,HRFlowable
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.graphics.shapes import Drawing,Rect,String
    buf=io.BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,leftMargin=2*cm,rightMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
    IND=HexColor("#6366f1"); ORG=HexColor("#f97316"); VIO=HexColor("#8b5cf6")
    GRN=HexColor("#10b981"); RED=HexColor("#ef4444"); YEL=HexColor("#f59e0b")
    DARK=HexColor("#0f1020"); GBG=HexColor("#f4f6fb"); GMID=HexColor("#e0e3f0"); TXT=HexColor("#1a1d2e"); MUT=HexColor("#6b7280")
    def sc(s): return GRN if s>=80 else HexColor("#84cc16") if s>=60 else YEL if s>=40 else ORG if s>=15 else RED
    def PS(n,**k): return ParagraphStyle(n,**k)
    B=PS("B",fontName="Helvetica-Bold",fontSize=9,textColor=TXT,leading=13)
    SM=PS("SM",fontName="Helvetica",fontSize=8,textColor=MUT,leading=11)
    story=[]
    now=datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    scores=data["scores"]; tests=data["tests"]; log=data["log"]
    streak=get_streak(log); total_h=sum(log.values())
    mastered=sum(1 for v in scores.values() if v==100); total_ch=len(scores)
    last=tests[-1] if tests else None
    if last:
        sj=last.get("scores_json") or "{}"; sd=json.loads(sj) if isinstance(sj,str) and sj.strip() else {}
        if not sd and last.get("physics") is not None: sd={"s1":last.get("physics",0),"s2":last.get("chemistry",0),"s3":last.get("maths",0)}
        pred=calc_pct(*sd.values())
    else: pred=None
    def sub_avg(s): v=[x for k,x in scores.items() if k.startswith(s)]; return round(sum(v)/len(v),1) if v else 0

    # Banner
    banner=Drawing(17*cm,2.8*cm)
    banner.add(Rect(0,0,17*cm,2.8*cm,fillColor=DARK,strokeColor=None,rx=8,ry=8))
    banner.add(Rect(0,0,3.5,2.8*cm,fillColor=IND,strokeColor=None))
    banner.add(String(16,2.0*cm,"StudyOS — Study Performance Report",fillColor=white,fontSize=14,fontName="Helvetica-Bold"))
    banner.add(String(16,1.3*cm,f"Student: {user.get('name') or user.get('username','')}  |  @{user.get('username','')}",fillColor=HexColor("#a5b4fc"),fontSize=9,fontName="Helvetica"))
    banner.add(String(16,0.6*cm,f"Generated: {now}",fillColor=HexColor("#6b7280"),fontSize=8,fontName="Helvetica"))
    story.append(banner); story.append(Spacer(1,0.4*cm))

    # KPIs
    def kpi(val,unit,label,col):
        return [Paragraph(f'<font color="{col.hexval()}" size="18"><b>{val}</b></font><font size="8" color="#6b7280"> {unit}</font>',PS("K",fontName="Helvetica",fontSize=9,leading=22)),
                Paragraph(f'<font size="8" color="#6b7280">{label}</font>',SM)]
    kt=Table([[kpi(f"{pred:.1f}" if pred else "—","%ile","Predicted Percentile",IND),
               kpi(str(streak),"days","Study Streak",ORG),
               kpi(f"{total_h:.0f}","h","Hours Logged",VIO),
               kpi(f"{mastered}/{total_ch}","","Chapters Mastered",GRN)]],colWidths=[4.1*cm]*4)
    kt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GBG),("BOX",(0,0),(-1,-1),0.5,GMID),("INNERGRID",(0,0),(-1,-1),0.5,GMID),("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),("LEFTPADDING",(0,0),(-1,-1),10),("VALIGN",(0,0),(-1,-1),"TOP")]))
    story.append(kt); story.append(Spacer(1,0.4*cm))

    # Subject mastery
    story.append(Paragraph('<font size="12" color="#6366f1"><b>Subject Mastery</b></font>',PS("H",fontName="Helvetica-Bold",fontSize=12,textColor=IND,leading=16,spaceAfter=8,spaceBefore=8)))
    for sub,col in [("Physics",IND),("Chemistry",ORG),("Maths",VIO)]:
        avg=sub_avg(sub)
        def mbar(w,h,pct,fc):
            d=Drawing(w,h); d.add(Rect(0,0,w,h,fillColor=GMID,strokeColor=None))
            fw=max(0,min(pct/100,1))*w
            if fw>0: d.add(Rect(0,0,fw,h,fillColor=fc,strokeColor=None))
            return d
        row=[Paragraph(f"<b>{sub}</b>",B),mbar(7*cm,10,avg,col),Paragraph(f"<b>{avg}%</b>",B)]
        t=Table([row],colWidths=[3*cm,7*cm,2*cm]); t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("BOTTOMPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),6)]))
        story.append(t)
    story.append(Spacer(1,0.3*cm))

    # Chapters table
    story.append(Paragraph('<font size="10" color="#1a1d2e"><b>Chapter Scores</b></font>',PS("H2",fontName="Helvetica-Bold",fontSize=10,textColor=TXT,leading=14,spaceAfter=6,spaceBefore=10)))
    rows=[["Chapter","Subject","Score","Status"]]
    exam_type=user.get("exam_type","JEE"); exam_subs=get_exam(exam_type)["subjects"]
    for sub in exam_subs:
        for t2 in exam_subs[sub]["topics"]:
            k=f"{sub}::{t2}"; sv=scores.get(k,0)
            st="Mastered" if sv==100 else "Strong" if sv>=80 else "Average" if sv>=50 else "Weak" if sv>0 else "Not Started"
            rows.append([Paragraph(t2,SM),Paragraph(sub,SM),Paragraph(f"<b>{sv}%</b>",SM),Paragraph(st,SM)])
    tbl=Table(rows,colWidths=[5*cm,2.5*cm,2*cm,3.5*cm],repeatRows=1)
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),IND),("TEXTCOLOR",(0,0),(-1,0),white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8),("ROWBACKGROUNDS",(0,1),(-1,-1),[white,GBG]),("GRID",(0,0),(-1,-1),0.3,GMID),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),5)]))
    story.append(tbl); story.append(Spacer(1,0.4*cm))

    # Mock tests
    story.append(Paragraph('<font size="12" color="#8b5cf6"><b>Mock Test History</b></font>',PS("H3",fontName="Helvetica-Bold",fontSize=12,textColor=VIO,leading=16,spaceAfter=8,spaceBefore=8)))
    if not tests:
        story.append(Paragraph("No mock tests recorded yet.",SM))
    else:
        tr=[["Date","Physics","Chemistry","Maths","Avg","Percentile"]]
        for t3 in reversed(tests[-10:]):
            avg2=(t3["physics"]+t3["chemistry"]+t3["maths"])/3
            tr.append([str(t3["date"]),f"{t3['physics']:.0f}%",f"{t3['chemistry']:.0f}%",f"{t3['maths']:.0f}%",f"{avg2:.1f}%",f"{t3['percentile']:.1f}%ile"])
        tt=Table(tr,colWidths=[3*cm,2.5*cm,2.5*cm,2*cm,2*cm,3*cm],repeatRows=1)
        tt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),VIO),("TEXTCOLOR",(0,0),(-1,0),white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8),("ROWBACKGROUNDS",(0,1),(-1,-1),[white,GBG]),("GRID",(0,0),(-1,-1),0.3,GMID),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),5)]))
        story.append(tt)

    story.append(Spacer(1,0.3*cm))
    story.append(HRFlowable(width="100%",thickness=1,color=GMID))
    story.append(Spacer(1,0.2*cm))
    story.append(Paragraph(f'<font size="7" color="#9ca3af">StudyOS Report · @{user.get("username","")} · {now} · Percentile estimates are AI-based projections.</font>',SM))
    doc.build(story)
    return buf.getvalue()

# ═══════════════════════════════════════════════════════════════════════
# HTTP SERVER
# ═══════════════════════════════════════════════════════════════════════
class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass

    def tok(self):
        for p in self.headers.get("Cookie","").split(";"):
            p=p.strip()
            if p.startswith("jt="):return p[3:]
        return None

    def me(self): return user_from_token(self.tok())

    def _safe_write(self,b):
        try:
            self.wfile.write(b)
        except (ConnectionAbortedError,ConnectionResetError,BrokenPipeError):
            pass

    def J(self,obj,code=200):
        b=json.dumps(obj,default=str).encode()
        self.send_response(code); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self._safe_write(b)

    def HTML(self,html):
        b=html.encode(); self.send_response(200); self.send_header("Content-Type","text/html;charset=utf-8"); self.send_header("Cache-Control","no-cache, no-store, must-revalidate"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self._safe_write(b)

    def BYTES(self,data,ct,fname=None):
        self.send_response(200); self.send_header("Content-Type",ct); self.send_header("Content-Length",str(len(data)))
        if fname: self.send_header("Content-Disposition",f'attachment;filename="{fname}"')
        self.end_headers(); self._safe_write(data)

    def body(self):
        n=int(self.headers.get("Content-Length",0))
        if not n: return {}
        raw=self.rfile.read(n)
        if "json" in self.headers.get("Content-Type",""): return json.loads(raw)
        return {}

    def cookie(self,t):
        self.send_header("Set-Cookie",f"jt={t}; Path=/; Max-Age=2592000; SameSite=Lax")

    def set_cookie_clear(self):
        self.send_header("Set-Cookie","jt=; Path=/; Max-Age=0")

    def do_OPTIONS(self):
        self.send_response(200)
        for k,v in [("Access-Control-Allow-Origin","*"),("Access-Control-Allow-Methods","GET,POST"),("Access-Control-Allow-Headers","Content-Type,Cookie")]:
            self.send_header(k,v)
        self.end_headers()

    def do_GET(self):
        path=urlparse(self.path).path; u=self.me()

        if path in("/","/index.html"):
            self.HTML(PAGE); return

        if path.startswith("/api/") and path not in("/api/login","/api/register"):
            if not u: self.J({"error":"Unauthorized"},401); return

        if path=="/api/state":
            uid=u["id"]; et=u.get("exam_type","JEE"); exam=get_exam(et)
            d=get_user_data(uid)
            sc=d["scores"]; log=d["log"]; tests=d["tests"]
            streak=get_streak(log); total_h=sum(log.values())
            last=tests[-1] if tests else None
            if last:
                sj=last.get("scores_json") or "{}"
                sdict=json.loads(sj) if isinstance(sj,str) and sj.strip() else {}
                if not sdict and last.get("physics") is not None:
                    subs=list(exam["subjects"].keys())
                    sdict={subs[0]:last.get("physics",0),subs[1]:last.get("chemistry",0),subs[min(2,len(subs)-1)]:last.get("maths",0)}
                pred=calc_pct(*sdict.values())
            else: pred=None
            plan=gen_plan(sc,d["priority"] or None)
            wt=weak_topics(sc,8)
            conn=db()
            try:
                frows=conn.execute("SELECT u.id,u.username,u.name,u.avatar FROM friends f JOIN users u ON u.id=f.friend_id WHERE f.user_id=? AND f.status='accepted'",(uid,)).fetchall()
                prows=conn.execute("SELECT u.username,u.name,u.avatar,f.created_at FROM friends f JOIN users u ON u.id=f.user_id WHERE f.friend_id=? AND f.status='pending'",(uid,)).fetchall()
            finally:
                conn.close()
            sub_names=list(exam["subjects"].keys())
            clean_tests=[]
            for t in tests:
                td=dict(t) if not isinstance(t,dict) else t
                sj2=td.get("scores_json") or "{}"
                sd2=json.loads(sj2) if isinstance(sj2,str) and sj2.strip() else {}
                if not sd2 and td.get("physics") is not None:
                    sd2={sub_names[0]:td.get("physics",0),sub_names[1]:td.get("chemistry",0),sub_names[min(2,len(sub_names)-1)]:td.get("maths",0)}
                td["scores"]=sd2; clean_tests.append(td)
            self.J({"user":{k:u[k] for k in["id","username","name","avatar","bio","college","exam_type","exam_date","theme","created_at","email"]},
                "exam_type":et,"exam":{"name":exam["name"],"icon":exam["icon"],"brand":exam["brand"],"brandHL":exam["brandHL"],"tagline":exam["tagline"],"tiers":exam["tiers"]},
                "topic_scores":sc,"checked":d["checked"],"mock_tests":clean_tests,"study_log":log,"priority":d["priority"],"activity":d["activity"],
                "streak":streak,"predicted_pct":pred,"daily_plan":plan,"weak_topics":wt,"total_hours":round(total_h,2),
                "subjects":exam["subjects"],"subtopics":exam["subtopics"],
                "friends":[dict(r) for r in frows],"pending":[dict(r) for r in prows],"changelog":CHANGELOG,"quotes":QUOTES,"exam_list":[{"key":k,"name":v["name"],"icon":v["icon"]} for k,v in EXAMS.items()]})
            return

        if path=="/api/report":
            d=get_user_data(u["id"])
            pdf=make_pdf(u,d)
            self.BYTES(pdf,"application/pdf",f"StudyOS_Report_{u['username']}_{datetime.date.today()}.pdf")
            log_act(u["id"],"Downloaded PDF report"); return

        if path.startswith("/api/friend_stats/"):
            fid=int(path.split("/")[-1])
            fd=get_user_data(fid)
            conn=db(); fu=conn.execute("SELECT username,name,avatar FROM users WHERE id=?",(fid,)).fetchone(); conn.close()
            if not fu: self.J({"error":"Not found"},404); return
            log2=fd["log"]; tests2=fd["tests"]
            if tests2:
                lt=tests2[-1]; sj=lt.get("scores_json") or "{}"; sd=json.loads(sj) if isinstance(sj,str) and sj.strip() else {}
                if not sd and lt.get("physics") is not None: sd={"s1":lt.get("physics",0),"s2":lt.get("chemistry",0),"s3":lt.get("maths",0)}
                pred2=calc_pct(*sd.values())
            else: pred2=None
            self.J({"username":fu["username"],"name":fu["name"],"avatar":fu["avatar"],"predicted_pct":pred2,"total_hours":sum(log2.values()),"mastered":sum(1 for v in fd["scores"].values() if v==100),"streak":get_streak(log2)}); return

        if path=="/api/doubts":
            qs=parse_qs(urlparse(self.path).query); sub=qs.get("subject",[None])[0]
            conn=db()
            q="SELECT d.*,u.username,u.name,u.avatar,(SELECT COUNT(*) FROM replies r WHERE r.doubt_id=d.id) AS replies FROM doubts d JOIN users u ON u.id=d.user_id"
            rows=conn.execute(q+(" WHERE d.subject=?" if sub and sub!="All" else "")+" ORDER BY d.created_at DESC LIMIT 60",(sub,) if sub and sub!="All" else ()).fetchall()
            conn.close(); self.J([dict(r) for r in rows]); return

        if path.startswith("/api/doubt/"):
            did=int(path.split("/")[-1]); conn=db()
            d=conn.execute("SELECT d.*,u.username,u.name,u.avatar FROM doubts d JOIN users u ON u.id=d.user_id WHERE d.id=?",(did,)).fetchone()
            reps=conn.execute("SELECT r.*,u.username,u.name,u.avatar FROM replies r JOIN users u ON u.id=r.user_id WHERE r.doubt_id=? ORDER BY r.created_at",(did,)).fetchall()
            conn.close()
            if not d: self.J({"error":"Not found"},404); return
            self.J({"doubt":dict(d),"replies":[dict(r) for r in reps]}); return

        if path.startswith("/api/profile/"):
            uname=path.split("/")[-1]; conn=db()
            pu=conn.execute("SELECT id,username,name,avatar,bio,college,created_at FROM users WHERE username=?",(uname,)).fetchone()
            conn.close()
            if not pu: self.J({"error":"Not found"},404); return
            pd=get_user_data(pu["id"]); tests3=pd["tests"]
            if tests3:
                lt3=tests3[-1]; sj3=lt3.get("scores_json") or "{}"; sd3=json.loads(sj3) if isinstance(sj3,str) and sj3.strip() else {}
                if not sd3 and lt3.get("physics") is not None: sd3={"s1":lt3.get("physics",0),"s2":lt3.get("chemistry",0),"s3":lt3.get("maths",0)}
                pred3=calc_pct(*sd3.values())
            else: pred3=None
            conn=db(); doubts=[dict(r) for r in conn.execute("SELECT id,title,subject,created_at,solved FROM doubts WHERE user_id=? ORDER BY created_at DESC LIMIT 10",(pu["id"],)).fetchall()]; conn.close()
            self.J({**dict(pu),"predicted_pct":pred3,"total_hours":sum(pd["log"].values()),"mastered":sum(1 for v in pd["scores"].values() if v==100),"doubts":doubts}); return

        self.send_response(404); self.end_headers()

    def do_POST(self):
        path=urlparse(self.path).path; b=self.body(); u=self.me()

        if path=="/api/register":
            un,dn,em,pw,pw2=b.get("username","").strip().lower(),b.get("name","").strip(),b.get("email","").strip().lower(),b.get("password",""),b.get("password2","")
            av=b.get("avatar","🎯"); et=b.get("exam_type","JEE")
            if et not in EXAMS: et="JEE"
            if len(un)<3: self.J({"error":"Username must be ≥ 3 characters"},400); return
            if len(pw)<6: self.J({"error":"Password must be ≥ 6 characters"},400); return
            if pw!=pw2:   self.J({"error":"Passwords do not match"},400); return
            if "@" not in em: self.J({"error":"Invalid email"},400); return
            salt,h=hp(pw)
            exam=get_exam(et)
            try:
                conn=db()
                try:
                    conn.execute("INSERT INTO users(username,email,pw_hash,pw_salt,name,avatar,exam_type) VALUES(?,?,?,?,?,?,?)",(un,em,h,salt,dn or un,av,et))
                    uid=conn.execute("SELECT id FROM users WHERE username=?",(un,)).fetchone()[0]
                    rows=[(uid,f"{s}::{t}",0) for s,d2 in exam["subjects"].items() for t in d2["topics"]]
                    conn.executemany("INSERT OR IGNORE INTO topic_scores(user_id,key,score) VALUES(?,?,?)",rows)
                    conn.commit()
                finally:
                    conn.close()
            except sqlite3.IntegrityError as e:
                self.J({"error":"Username or email already taken"},400); return
            tok=make_token(uid); log_act(uid,"Account created",f"Welcome, {dn or un}!")
            self.send_response(200); self.send_header("Content-Type","application/json"); self.cookie(tok)
            out=json.dumps({"ok":True}).encode(); self.send_header("Content-Length",str(len(out))); self.end_headers(); self._safe_write(out); return

        if path=="/api/login":
            un=b.get("username","").lower().strip(); pw=b.get("password","")
            conn=db()
            try:
                row=conn.execute("SELECT * FROM users WHERE username=? OR email=?",(un,un)).fetchone()
            finally:
                conn.close()
            if not row or not (lambda s,h,p: hashlib.pbkdf2_hmac("sha256",p.encode(),s.encode(),260000).hex()==h)(row["pw_salt"],row["pw_hash"],pw):
                self.J({"error":"Invalid username or password"},401); return
            tok=make_token(row["id"]); log_act(row["id"],"Logged in")
            self.send_response(200); self.send_header("Content-Type","application/json"); self.cookie(tok)
            out=json.dumps({"ok":True}).encode(); self.send_header("Content-Length",str(len(out))); self.end_headers(); self._safe_write(out); return

        if not u: self.J({"error":"Unauthorized"},401); return
        uid=u["id"]

        if path=="/api/logout":
            conn=db()
            try:
                conn.execute("DELETE FROM sessions WHERE token=?",(self.tok(),)); conn.commit()
            finally:
                conn.close()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.set_cookie_clear()
            out=json.dumps({"ok":True}).encode(); self.send_header("Content-Length",str(len(out))); self.end_headers(); self._safe_write(out); return

        if path=="/api/profile/update":
            fields=["name","avatar","bio","college","exam_type","exam_date","theme"]
            sets=[f"{f}=?" for f in fields if f in b]; vals=[b[f] for f in fields if f in b]
            if sets:
                conn=db(); conn.execute(f"UPDATE users SET {','.join(sets)} WHERE id=?",vals+[uid]); conn.commit(); conn.close()
            if "new_password" in b and b.get("new_password"):
                np=b["new_password"]
                if len(np)<6: self.J({"error":"Password must be ≥ 6 characters"},400); return
                op=b.get("old_password","")
                conn=db(); row=conn.execute("SELECT pw_hash,pw_salt FROM users WHERE id=?",(uid,)).fetchone(); conn.close()
                if not (lambda s,h,p: hashlib.pbkdf2_hmac("sha256",p.encode(),s.encode(),260000).hex()==h)(row["pw_salt"],row["pw_hash"],op):
                    self.J({"error":"Current password is incorrect"},400); return
                salt,h2=hp(np); conn=db(); conn.execute("UPDATE users SET pw_hash=?,pw_salt=? WHERE id=?",(h2,salt,uid)); conn.commit(); conn.close()
            if "exam_type" in b and b["exam_type"]:
                new_et=b["exam_type"]
                new_exam=get_exam(new_et)
                conn2=db()
                try:
                    for sub in new_exam["subjects"]:
                        for ch in new_exam["subjects"][sub]["topics"]:
                            ck=f"{sub}::{ch}"
                            existing=conn2.execute("SELECT score FROM topic_scores WHERE user_id=? AND key=?",(uid,ck)).fetchone()
                            if not existing:
                                conn2.execute("INSERT OR IGNORE INTO topic_scores(user_id,key,score) VALUES(?,?,0)",(uid,ck,0))
                    conn2.commit()
                finally:
                    conn2.close()
            self.J({"ok":True}); return

        if path=="/api/delete_account":
            pw=b.get("password","")
            conn=db()
            try:
                row=conn.execute("SELECT pw_hash,pw_salt FROM users WHERE id=?",(uid,)).fetchone()
                if not row: self.J({"error":"User not found"},404); return
                if not (lambda s,h,p: hashlib.pbkdf2_hmac("sha256",p.encode(),s.encode(),260000).hex()==h)(row["pw_salt"],row["pw_hash"],pw):
                    self.J({"error":"Incorrect password"},400); return
                conn.execute("DELETE FROM users WHERE id=?",(uid,))
                conn.commit()
            finally:
                conn.close()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.set_cookie_clear()
            out=json.dumps({"ok":True}).encode(); self.send_header("Content-Length",str(len(out))); self.end_headers(); self._safe_write(out); return

        if path=="/api/toggle_sub":
            sub,ch,st=b["subject"],b["chapter"],b["subtopic"]
            et=u.get("exam_type","JEE"); exam_st=get_exam(et).get("subtopics",{})
            ck=f"{sub}::{ch}"; sk=f"{ck}::{st}"; all_s=exam_st.get(ck,[])
            conn=db()
            cur=conn.execute("SELECT val FROM checked WHERE user_id=? AND key=?",(uid,sk)).fetchone()
            nv=0 if(cur and cur["val"]) else 1
            conn.execute("INSERT OR REPLACE INTO checked(user_id,key,val) VALUES(?,?,?)",(uid,sk,nv))
            done=conn.execute("SELECT COUNT(*) FROM checked WHERE user_id=? AND key LIKE ? AND val=1",(uid,f"{ck}::%")).fetchone()[0]
            score=round((done/len(all_s))*100) if all_s else 0
            conn.execute("INSERT OR REPLACE INTO topic_scores(user_id,key,score) VALUES(?,?,?)",(uid,ck,score))
            conn.commit(); conn.close()
            self.J({"score":score,"checked":bool(nv)}); return

        if path=="/api/toggle_all":
            sub,ch=b["subject"],b["chapter"]; ck=f"{sub}::{ch}"
            et=u.get("exam_type","JEE"); all_s=get_exam(et).get("subtopics",{}).get(ck,[])
            conn=db()
            done=conn.execute("SELECT COUNT(*) FROM checked WHERE user_id=? AND key LIKE ? AND val=1",(uid,f"{ck}::%")).fetchone()[0]
            nv=0 if done==len(all_s) else 1
            for s in all_s: conn.execute("INSERT OR REPLACE INTO checked(user_id,key,val) VALUES(?,?,?)",(uid,f"{ck}::{s}",nv))
            conn.execute("INSERT OR REPLACE INTO topic_scores(user_id,key,score) VALUES(?,?,?)",(uid,ck,100 if nv else 0))
            conn.commit(); conn.close()
            self.J({"score":100 if nv else 0}); return

        if path=="/api/log_hours":
            date=b.get("date",datetime.date.today().isoformat()); hrs=float(b.get("hours",0))
            if hrs>0:
                conn=db(); cur=conn.execute("SELECT hours FROM study_log WHERE user_id=? AND date=?",(uid,date)).fetchone()
                conn.execute("INSERT OR REPLACE INTO study_log(user_id,date,hours) VALUES(?,?,?)",(uid,date,round((cur["hours"] if cur else 0)+hrs,2)))
                conn.commit(); conn.close()
            self.J({"ok":True}); return

        if path=="/api/set_hours":
            date=b["date"]; hrs=float(b.get("hours",0)); conn=db()
            if hrs>0: conn.execute("INSERT OR REPLACE INTO study_log(user_id,date,hours) VALUES(?,?,?)",(uid,date,round(hrs,2)))
            else: conn.execute("DELETE FROM study_log WHERE user_id=? AND date=?",(uid,date))
            conn.commit(); conn.close(); self.J({"ok":True}); return

        if path=="/api/add_test":
            scores=b.get("scores",{})
            if not scores:
                scores={"Physics":float(b.get("physics",0)),"Chemistry":float(b.get("chemistry",0)),"Maths":float(b.get("maths",0))}
            scores={k:float(v) for k,v in scores.items()}
            date=b.get("date",datetime.date.today().isoformat()); pct=calc_pct(*scores.values())
            sj=json.dumps(scores); vals=list(scores.values())
            p,c,m=(vals+[0,0,0])[:3]
            conn=db()
            try:
                cur=conn.execute("INSERT INTO mock_tests(user_id,date,physics,chemistry,maths,scores_json,percentile,notes) VALUES(?,?,?,?,?,?,?,?)",(uid,date,p,c,m,sj,pct,b.get("notes","")))
                conn.commit(); tid=cur.lastrowid
            finally:
                conn.close()
            log_act(uid,"Added mock test",f"{date}: {pct:.1f}%ile")
            self.J({"ok":True,"id":tid,"percentile":pct,"scores":scores}); return

        if path=="/api/edit_test":
            scores=b.get("scores",{})
            if not scores:
                scores={"Physics":float(b.get("physics",0)),"Chemistry":float(b.get("chemistry",0)),"Maths":float(b.get("maths",0))}
            scores={k:float(v) for k,v in scores.items()}
            pct=calc_pct(*scores.values()); sj=json.dumps(scores); vals=list(scores.values())
            p,c,m=(vals+[0,0,0])[:3]
            conn=db()
            try:
                conn.execute("UPDATE mock_tests SET physics=?,chemistry=?,maths=?,scores_json=?,percentile=?,date=COALESCE(?,date) WHERE id=? AND user_id=?",(p,c,m,sj,pct,b.get("date"),int(b["id"]),uid))
                conn.commit()
            finally:
                conn.close()
            self.J({"ok":True,"percentile":pct}); return

        if path=="/api/del_test":
            conn=db(); conn.execute("DELETE FROM mock_tests WHERE id=? AND user_id=?",(int(b["id"]),uid)); conn.commit(); conn.close()
            self.J({"ok":True}); return

        if path=="/api/clear_tests":
            conn=db(); conn.execute("DELETE FROM mock_tests WHERE user_id=?",(uid,)); conn.commit(); conn.close()
            self.J({"ok":True}); return

        if path=="/api/set_priority":
            keys=b.get("keys",[]); conn=db()
            conn.execute("DELETE FROM priority WHERE user_id=?",(uid,))
            for i,k in enumerate(keys): conn.execute("INSERT INTO priority(user_id,key,pos) VALUES(?,?,?)",(uid,k,i))
            conn.commit(); conn.close(); log_act(uid,"Updated priority queue"); self.J({"ok":True}); return

        if path=="/api/boost":
            key=b["key"]; delta=int(b.get("delta",5)); conn=db()
            cur=conn.execute("SELECT score FROM topic_scores WHERE user_id=? AND key=?",(uid,key)).fetchone()
            ns=min(100,max(0,(cur["score"] if cur else 0)+delta))
            conn.execute("INSERT OR REPLACE INTO topic_scores(user_id,key,score) VALUES(?,?,?)",(uid,key,ns))
            conn.commit(); conn.close(); self.J({"score":ns}); return

        if path=="/api/add_friend":
            fn=b.get("username","").lower().strip(); conn=db()
            fu=conn.execute("SELECT id FROM users WHERE username=?",(fn,)).fetchone()
            if not fu: conn.close(); self.J({"error":"User not found"},404); return
            fid=fu["id"]
            if fid==uid: conn.close(); self.J({"error":"You can't add yourself"},400); return
            ex=conn.execute("SELECT status FROM friends WHERE user_id=? AND friend_id=?",(uid,fid)).fetchone()
            if ex: conn.close(); self.J({"error":f"Request already {ex['status']}"},400); return
            conn.execute("INSERT INTO friends(user_id,friend_id,status) VALUES(?,?,'pending')",(uid,fid))
            conn.commit(); conn.close(); log_act(uid,"Sent friend request",f"To @{fn}"); self.J({"ok":True}); return

        if path=="/api/accept_friend":
            fn=b.get("username","").lower(); conn=db()
            fu=conn.execute("SELECT id FROM users WHERE username=?",(fn,)).fetchone()
            if not fu: conn.close(); self.J({"error":"Not found"},404); return
            fid=fu["id"]
            conn.execute("UPDATE friends SET status='accepted' WHERE user_id=? AND friend_id=?",(fid,uid))
            conn.execute("INSERT OR IGNORE INTO friends(user_id,friend_id,status) VALUES(?,?,'accepted')",(uid,fid))
            conn.commit(); conn.close(); log_act(uid,"Accepted friend request",f"@{fn}"); self.J({"ok":True}); return

        if path=="/api/remove_friend":
            fid=int(b["friend_id"]); conn=db()
            conn.execute("DELETE FROM friends WHERE (user_id=? AND friend_id=?) OR (user_id=? AND friend_id=?)",(uid,fid,fid,uid))
            conn.commit(); conn.close(); self.J({"ok":True}); return

        if path=="/api/post_doubt":
            title=b.get("title","").strip(); body2=b.get("body","").strip()
            if not title or not body2: self.J({"error":"Title and body required"},400); return
            conn=db(); cur=conn.execute("INSERT INTO doubts(user_id,title,body,subject,media_type,media_b64) VALUES(?,?,?,?,?,?)",(uid,title,body2,b.get("subject","General"),b.get("media_type","none"),b.get("media_b64","")))
            conn.commit(); did=cur.lastrowid; conn.close()
            log_act(uid,"Posted doubt",title); self.J({"ok":True,"id":did}); return

        if path=="/api/edit_doubt":
            did=int(b["id"]); conn=db()
            conn.execute("UPDATE doubts SET title=?,body=?,subject=?,updated_at=datetime('now') WHERE id=? AND user_id=?",(b.get("title",""),b.get("body",""),b.get("subject","General"),did,uid))
            conn.commit(); conn.close(); self.J({"ok":True}); return

        if path=="/api/solve_doubt":
            conn=db(); conn.execute("UPDATE doubts SET solved=1-solved WHERE id=? AND user_id=?",(int(b["id"]),uid)); conn.commit(); conn.close(); self.J({"ok":True}); return

        if path=="/api/del_doubt":
            conn=db(); conn.execute("DELETE FROM doubts WHERE id=? AND user_id=?",(int(b["id"]),uid)); conn.commit(); conn.close(); self.J({"ok":True}); return

        if path=="/api/post_reply":
            body2=b.get("body","").strip()
            if not body2: self.J({"error":"Reply cannot be empty"},400); return
            conn=db(); conn.execute("INSERT INTO replies(doubt_id,user_id,body) VALUES(?,?,?)",(int(b["doubt_id"]),uid,body2)); conn.commit(); conn.close()
            log_act(uid,"Replied to doubt",f"Doubt #{b['doubt_id']}"); self.J({"ok":True}); return

        if path=="/api/edit_reply":
            conn=db(); conn.execute("UPDATE replies SET body=?,updated_at=datetime('now') WHERE id=? AND user_id=?",(b.get("body",""),int(b["id"]),uid)); conn.commit(); conn.close(); self.J({"ok":True}); return

        if path=="/api/del_reply":
            conn=db(); conn.execute("DELETE FROM replies WHERE id=? AND user_id=?",(int(b["id"]),uid)); conn.commit(); conn.close(); self.J({"ok":True}); return

        self.J({"error":"Not found"},404)

# ═══════════════════════════════════════════════════════════════════════
# HTML PAGE
# ═══════════════════════════════════════════════════════════════════════
PAGE = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>StudyOS — Multi Study Platform</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;0,14..32,800;0,14..32,900;1,14..32,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
/* ══ DESIGN SYSTEM ══ */
:root{
  --f:'Inter',system-ui,-apple-system,sans-serif;
  --m:'JetBrains Mono',monospace;
  --r:10px;--r2:14px;--r3:20px;--r4:28px;
  --phy:#818cf8;--che:#fb923c;--mat:#a78bfa;
  --grn:#34d399;--yel:#fbbf24;--red:#f87171;--blu:#60a5fa;--pink:#f472b6;--cyan:#22d3ee;
  --acc:#818cf8;--acc2:#a78bfa;--acc3:#c084fc;
  --sh:0 1px 3px rgba(0,0,0,.06),0 4px 16px rgba(0,0,0,.04);
  --sh2:0 8px 32px rgba(0,0,0,.1),0 2px 6px rgba(0,0,0,.04);
  --sh3:0 24px 80px rgba(0,0,0,.18),0 4px 12px rgba(0,0,0,.06);
  --sh-glow:0 0 40px rgba(129,140,248,.15),0 0 80px rgba(167,139,250,.08);
  --tr:all .2s cubic-bezier(.4,0,.2,1);
  --tr-spring:all .4s cubic-bezier(.34,1.56,.64,1);
  --tr-smooth:all .35s cubic-bezier(.25,.46,.45,.94);
  --glass:rgba(255,255,255,.03);
  --glass-bd:rgba(255,255,255,.06);
}
[data-theme=dark]{
  --bg:#06060c;--bg1:#0c0c16;--bg2:#111120;--bg3:#16162a;
  --sr:rgba(20,20,40,.65);--sr2:rgba(28,28,52,.55);--sr3:rgba(36,36,64,.5);
  --bd:rgba(255,255,255,.06);--bd2:rgba(255,255,255,.1);
  --tx:#f0f0ff;--tx2:#a0a4cc;--tx3:#585c88;
  --inv:#06060c;
  --glass:rgba(255,255,255,.03);--glass-bd:rgba(255,255,255,.06);
}
[data-theme=light]{
  --bg:#f4f4fc;--bg1:#ecedf8;--bg2:#e4e5f2;--bg3:#dcdeed;
  --sr:rgba(255,255,255,.72);--sr2:rgba(240,241,252,.7);--sr3:rgba(228,229,245,.65);
  --bd:rgba(0,0,0,.07);--bd2:rgba(0,0,0,.11);
  --tx:#0c0c1a;--tx2:#3a3d5c;--tx3:#7a7ea6;
  --inv:#ffffff;
  --glass:rgba(255,255,255,.55);--glass-bd:rgba(255,255,255,.45);
}

/* ══ RESET ══ */
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;font-size:15px}
body{font-family:var(--f);background:var(--bg);color:var(--tx);min-height:100vh;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;z-index:-1;background:
  radial-gradient(ellipse 80% 60% at 10% 20%,rgba(129,140,248,.07),transparent),
  radial-gradient(ellipse 70% 50% at 90% 80%,rgba(167,139,250,.06),transparent),
  radial-gradient(ellipse 50% 40% at 50% 50%,rgba(192,132,252,.04),transparent);
  pointer-events:none}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:99px}
::-webkit-scrollbar-thumb:hover{background:var(--acc)}
a{color:inherit;text-decoration:none}
button,input,textarea,select{font-family:var(--f)}
button{cursor:pointer}
img{max-width:100%}

/* ══ ANIMATIONS ══ */
@keyframes up{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes in{from{opacity:0}to{opacity:1}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
@keyframes spin{to{stroke-dashoffset:0}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
@keyframes glow-pulse{0%,100%{box-shadow:0 0 20px rgba(129,140,248,.15)}50%{box-shadow:0 0 40px rgba(129,140,248,.3)}}
@keyframes slide-in{from{opacity:0;transform:translateY(20px) scale(.96)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes orbit{0%{transform:rotate(0deg) translateX(180px) rotate(0deg)}100%{transform:rotate(360deg) translateX(180px) rotate(-360deg)}}
.up{animation:slide-in .4s cubic-bezier(.4,0,.2,1) both}
.in{animation:in .25s ease both}

/* ══ AUTH ══ */
#auth{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;padding:1rem;transition:opacity .4s,transform .4s;overflow:hidden}
#auth::before{content:'';position:absolute;inset:0;background:
  radial-gradient(ellipse 60% 50% at 20% 30%,rgba(129,140,248,.12),transparent 60%),
  radial-gradient(ellipse 50% 60% at 80% 70%,rgba(192,132,252,.1),transparent 60%),
  radial-gradient(ellipse 40% 40% at 50% 10%,rgba(34,211,238,.06),transparent 50%),
  var(--bg);z-index:-2}
#auth::after{content:'';position:absolute;width:400px;height:400px;border-radius:50%;border:1px solid rgba(129,140,248,.08);top:50%;left:50%;transform:translate(-50%,-50%);z-index:-1;animation:glow-pulse 4s ease-in-out infinite}
#auth.gone{opacity:0;transform:scale(1.02);pointer-events:none}
.auth-orb{position:absolute;border-radius:50%;filter:blur(60px);opacity:.15;pointer-events:none;z-index:-1}
.auth-orb-1{width:300px;height:300px;background:var(--acc);top:-80px;left:-80px;animation:float 8s ease-in-out infinite}
.auth-orb-2{width:250px;height:250px;background:var(--acc3);bottom:-60px;right:-60px;animation:float 6s ease-in-out infinite 1s}
.auth-orb-3{width:150px;height:150px;background:var(--cyan);top:50%;right:20%;animation:float 10s ease-in-out infinite 2s}
.auth-card{width:100%;max-width:420px;background:var(--sr);border:1px solid var(--glass-bd);border-radius:var(--r4);padding:2.5rem;box-shadow:var(--sh3),var(--sh-glow);backdrop-filter:blur(40px);-webkit-backdrop-filter:blur(40px);position:relative}
.auth-logo{text-align:center;margin-bottom:2rem}
.auth-icon{width:56px;height:56px;border-radius:16px;background:linear-gradient(135deg,var(--acc),var(--acc3));display:flex;align-items:center;justify-content:center;font-size:1.6rem;margin:0 auto .7rem;box-shadow:0 8px 24px rgba(129,140,248,.35);animation:float 4s ease-in-out infinite;position:relative}
.auth-icon::after{content:'';position:absolute;inset:-4px;border-radius:20px;border:1.5px solid rgba(129,140,248,.2);animation:glow-pulse 3s ease-in-out infinite}
.auth-brand{font-size:1.55rem;font-weight:800;letter-spacing:-.04em;background:linear-gradient(135deg,var(--tx),var(--acc));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.auth-brand span{background:linear-gradient(135deg,var(--acc),var(--acc3));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.auth-tagline{font-size:.78rem;color:var(--tx3);margin-top:.3rem;font-weight:500;letter-spacing:.02em}
.auth-tabs{display:flex;background:var(--bg1);border-radius:12px;padding:.3rem;margin-bottom:1.75rem;gap:.3rem;border:1px solid var(--bd)}
.auth-tab{flex:1;padding:.52rem;border-radius:9px;border:none;background:transparent;color:var(--tx3);font-size:.82rem;font-weight:600;transition:var(--tr);position:relative}
.auth-tab.on{background:linear-gradient(135deg,rgba(129,140,248,.12),rgba(167,139,250,.08));color:var(--tx);box-shadow:var(--sh);border:1px solid var(--bd)}
.fg{margin-bottom:.95rem}
.fl{display:block;font-size:.72rem;font-weight:700;color:var(--tx2);margin-bottom:.4rem;letter-spacing:.03em;text-transform:uppercase}
.fi{width:100%;padding:.62rem .9rem;background:var(--bg1);border:1.5px solid var(--bd);border-radius:12px;color:var(--tx);font-size:.88rem;outline:none;transition:var(--tr)}
.fi:focus{border-color:var(--acc);box-shadow:0 0 0 3px rgba(129,140,248,.12),0 0 20px rgba(129,140,248,.06)}
.fi::placeholder{color:var(--tx3)}
.fr{display:grid;grid-template-columns:1fr 1fr;gap:.7rem}
.auth-btn{width:100%;padding:.75rem;background:linear-gradient(135deg,var(--acc),var(--acc3));border:none;border-radius:12px;color:#fff;font-size:.9rem;font-weight:700;transition:var(--tr);margin-top:.6rem;letter-spacing:.01em;position:relative;overflow:hidden}
.auth-btn::before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.15),transparent);transform:translateX(-100%);transition:transform .5s}
.auth-btn:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(129,140,248,.35)}
.auth-btn:hover::before{transform:translateX(100%)}
.auth-btn:active{transform:translateY(0)}
.auth-err{background:rgba(248,113,113,.08);border:1px solid rgba(248,113,113,.2);border-radius:12px;padding:.65rem .85rem;font-size:.8rem;color:var(--red);margin-bottom:.7rem;display:none;backdrop-filter:blur(8px)}
.emo-grid{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.4rem}
.emo-opt{width:2.15rem;height:2.15rem;border-radius:10px;border:1.5px solid var(--bd);background:var(--bg1);font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:var(--tr-spring)}
.emo-opt:hover{transform:scale(1.15);border-color:var(--acc)}
.emo-opt.on{border-color:var(--acc);background:rgba(129,140,248,.12);transform:scale(1.1);box-shadow:0 0 12px rgba(129,140,248,.2)}

/* ══ LAYOUT ══ */
#app{display:flex;flex-direction:column;min-height:100vh}
.wrap{max-width:1400px;margin:0 auto;width:100%;padding:0 1.5rem}
main{padding:1.75rem 0;flex:1}

/* ══ HEADER ══ */
header{position:sticky;top:0;z-index:100;height:60px;background:rgba(6,6,12,.7);border-bottom:1px solid var(--bd);backdrop-filter:blur(24px) saturate(1.4);-webkit-backdrop-filter:blur(24px) saturate(1.4)}
[data-theme=light] header{background:rgba(244,244,252,.8)}
.hdr{display:flex;align-items:center;height:60px;gap:.85rem}
.brand{display:flex;align-items:center;gap:.65rem;flex-shrink:0;cursor:pointer;transition:var(--tr)}
.brand:hover{opacity:.85}
.brand-icon{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,var(--acc),var(--acc3));display:flex;align-items:center;justify-content:center;font-size:1rem;box-shadow:0 4px 16px rgba(129,140,248,.35);position:relative}
.brand-icon::after{content:'';position:absolute;inset:0;border-radius:10px;box-shadow:inset 0 1px 0 rgba(255,255,255,.15);pointer-events:none}
.brand-name{font-size:1.15rem;font-weight:800;letter-spacing:-.03em}
.brand-name span{background:linear-gradient(135deg,var(--acc),var(--acc3));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hpills{display:flex;gap:.45rem;flex:1;overflow-x:auto;scrollbar-width:none}
.hpills::-webkit-scrollbar{display:none}
.hp{display:flex;align-items:center;gap:.3rem;padding:.2rem .65rem;border-radius:99px;border:1px solid;font-family:var(--m);font-size:.72rem;font-weight:500;white-space:nowrap;flex-shrink:0;backdrop-filter:blur(8px)}
.hright{display:flex;align-items:center;gap:.45rem;flex-shrink:0;position:relative}
.ibtn{width:36px;height:36px;border-radius:11px;background:var(--glass);border:1px solid var(--bd);display:flex;align-items:center;justify-content:center;font-size:.95rem;transition:var(--tr);cursor:pointer;position:relative;flex-shrink:0;backdrop-filter:blur(8px)}
.ibtn:hover{background:var(--sr2);border-color:var(--bd2);transform:translateY(-1px)}
.av{width:36px;height:36px;border-radius:11px;background:linear-gradient(135deg,var(--acc),var(--acc3));display:flex;align-items:center;justify-content:center;font-size:1rem;border:2px solid transparent;transition:var(--tr-spring);cursor:pointer;font-weight:700;color:#fff;flex-shrink:0}
.av:hover{border-color:var(--acc);box-shadow:0 0 0 3px rgba(129,140,248,.2);transform:scale(1.08)}
.bdg{position:absolute;top:-4px;right:-4px;width:17px;height:17px;border-radius:50%;background:var(--red);color:#fff;font-size:.58rem;font-weight:700;display:flex;align-items:center;justify-content:center;border:2px solid var(--bg);animation:pulse 2s ease-in-out infinite}

/* ══ DROPDOWN ══ */
.dd{position:absolute;top:calc(100% + .6rem);right:0;min-width:230px;background:var(--sr);border:1px solid var(--glass-bd);border-radius:16px;box-shadow:var(--sh3);padding:.5rem;z-index:300;display:none;animation:slide-in .2s ease;backdrop-filter:blur(40px);-webkit-backdrop-filter:blur(40px)}
.dd.on{display:block}
.dd-hdr{padding:.5rem .7rem .7rem;border-bottom:1px solid var(--bd);margin-bottom:.35rem}
.dd-name{font-weight:700;font-size:.9rem}
.dd-email{font-size:.72rem;color:var(--tx3);margin-top:.12rem;font-family:var(--m)}
.dd-item{display:flex;align-items:center;gap:.6rem;padding:.52rem .7rem;border-radius:10px;font-size:.82rem;color:var(--tx2);font-weight:500;transition:var(--tr);cursor:pointer}
.dd-item:hover{background:rgba(129,140,248,.06);color:var(--tx);transform:translateX(2px)}
.dd-item.red{color:var(--red)}
.dd-item.red:hover{background:rgba(248,113,113,.06)}
.dd-sep{height:1px;background:var(--bd);margin:.35rem 0}

/* ══ WHATS NEW ══ */
.wn{position:absolute;top:calc(100% + .6rem);right:0;width:320px;background:var(--sr);border:1px solid var(--glass-bd);border-radius:16px;box-shadow:var(--sh3);padding:1.1rem;z-index:300;display:none;animation:slide-in .2s ease;max-height:420px;overflow-y:auto;backdrop-filter:blur(40px)}
.wn.on{display:block}
.wn-hdr{font-size:.92rem;font-weight:700;margin-bottom:.8rem;display:flex;align-items:center;gap:.45rem}
.wn-item{padding:.65rem 0;border-bottom:1px solid var(--bd)}
.wn-item:last-child{border-bottom:none;padding-bottom:0}
.wn-ver{font-size:.68rem;font-weight:700;color:var(--acc);font-family:var(--m);margin-bottom:.2rem}
.wn-title{font-size:.82rem;font-weight:700;color:var(--tx);margin-bottom:.18rem}
.wn-body{font-size:.76rem;color:var(--tx2);line-height:1.55}

/* ══ NAV ══ */
nav{background:var(--bg1);border-bottom:1px solid var(--bd);overflow-x:auto;scrollbar-width:none;position:relative}
nav::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--acc),transparent);opacity:.15}
nav::-webkit-scrollbar{display:none}
.nav-inner{display:flex;height:46px}
.nb{display:flex;align-items:center;gap:.4rem;padding:0 1.05rem;border:none;background:transparent;color:var(--tx3);font-size:.8rem;font-weight:600;white-space:nowrap;border-bottom:2.5px solid transparent;transition:var(--tr);letter-spacing:.01em;position:relative}
.nb:hover{color:var(--tx2);background:rgba(129,140,248,.04)}
.nb.on{color:var(--acc);border-bottom-color:var(--acc)}
.nb.on::before{content:'';position:absolute;bottom:-1px;left:20%;right:20%;height:2px;background:var(--acc);filter:blur(4px)}

/* ══ CARDS ══ */
.card{background:var(--sr);border:1px solid var(--bd);border-radius:16px;padding:1.4rem;position:relative;overflow:hidden;transition:var(--tr);backdrop-filter:blur(20px)}
.card:hover{border-color:var(--bd2);box-shadow:var(--sh2);transform:translateY(-2px)}
.flat{background:var(--sr);border:1px solid var(--bd);border-radius:16px;padding:1.4rem;position:relative;overflow:hidden;backdrop-filter:blur(20px)}
.card-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.1rem}
.kpi{padding:1.2rem;position:relative}
.kpi::before{content:'';position:absolute;top:0;right:0;width:80px;height:80px;border-radius:50%;opacity:.06;background:var(--acc);filter:blur(20px)}
.kv{font-size:2.1rem;font-weight:800;line-height:1;letter-spacing:-.04em;background:linear-gradient(135deg,var(--tx),var(--tx2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.ku{font-size:.8rem;font-weight:500;color:var(--tx3);margin-left:.15rem}
.ks{font-size:.73rem;color:var(--tx3);font-weight:500;margin-top:.25rem}
.deco{position:absolute;top:-15px;right:-15px;width:90px;height:90px;border-radius:50%;opacity:.08;filter:blur(8px)}

/* ══ GRIDS ══ */
.g-kpi{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem}
.g-3{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.g-2{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem}
.g-a{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.8rem}
.g-ch{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.8rem}
.g-sub{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:.55rem}
.g-plan{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem}
.g-cal{display:grid;grid-template-columns:repeat(10,1fr);gap:4px}
.flex{display:flex}.fc{display:flex;flex-direction:column}
.gap-xs{gap:.35rem}.gap-s{gap:.55rem}.gap-m{gap:.9rem}.gap-l{gap:1.35rem}
.wrap-f{flex-wrap:wrap}.btwn{justify-content:space-between}.ctr{align-items:center}.start{align-items:flex-start}
.mt-s{margin-top:.5rem}.mt-m{margin-top:.9rem}.mt-l{margin-top:1.35rem}
.mb-s{margin-bottom:.5rem}.mb-m{margin-bottom:.9rem}.mb-l{margin-bottom:1.35rem}
.full{width:100%}.hide{display:none!important}

/* ══ BUTTONS ══ */
.btn{display:inline-flex;align-items:center;gap:.4rem;padding:.5rem 1.05rem;border-radius:11px;font-size:.8rem;font-weight:600;border:1.5px solid;transition:var(--tr);white-space:nowrap;letter-spacing:.01em;position:relative;overflow:hidden}
.btn:hover{transform:translateY(-2px)}
.btn:active{transform:translateY(0);transition:transform .05s}
.bf{background:linear-gradient(135deg,var(--acc),var(--acc2));border-color:transparent;color:#fff;box-shadow:0 4px 14px rgba(129,140,248,.25)}
.bf:hover{box-shadow:0 6px 20px rgba(129,140,248,.35)}
.bo{background:var(--glass);border-color:var(--bd2);color:var(--tx2);backdrop-filter:blur(8px)}
.bo:hover{border-color:var(--acc);color:var(--acc);background:rgba(129,140,248,.06)}
.bd2{background:rgba(248,113,113,.08);border-color:rgba(248,113,113,.25);color:var(--red)}
.bd2:hover{background:rgba(248,113,113,.12);box-shadow:0 4px 14px rgba(248,113,113,.15)}
.bs{background:rgba(52,211,153,.08);border-color:rgba(52,211,153,.25);color:var(--grn)}
.bs:hover{box-shadow:0 4px 14px rgba(52,211,153,.15)}
.bsm{padding:.3rem .7rem;font-size:.74rem;border-radius:9px}
.bxs{padding:.18rem .5rem;font-size:.68rem;border-radius:7px}
.bw{padding:.65rem 1.7rem}

/* ══ INPUTS ══ */
.inp{width:100%;padding:.58rem .9rem;background:var(--bg1);border:1.5px solid var(--bd);border-radius:12px;color:var(--tx);font-size:.86rem;outline:none;transition:var(--tr)}
.inp:focus{border-color:var(--acc);box-shadow:0 0 0 3px rgba(129,140,248,.1),0 0 16px rgba(129,140,248,.05)}
.inp::placeholder{color:var(--tx3)}
.inp-sm{padding:.4rem .72rem;font-size:.8rem;border-radius:9px}
textarea.inp{resize:vertical;min-height:85px;line-height:1.55}
select.inp{cursor:pointer}

/* ══ CHIPS ══ */
.chip{display:inline-flex;align-items:center;padding:.2rem .62rem;border-radius:99px;font-size:.68rem;font-weight:700;letter-spacing:.04em;border:1px solid;backdrop-filter:blur(4px)}

/* ══ BAR ══ */
.bt{background:var(--bd);border-radius:99px;overflow:hidden}
.bf2{height:100%;border-radius:99px;transition:width .6s cubic-bezier(.34,1.56,.64,1);position:relative}
.bf2::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.15),transparent);animation:shimmer 2s ease-in-out infinite}

/* ══ SUB TABS ══ */
.stabs{display:flex;gap:.3rem;background:var(--bg1);border-radius:12px;padding:.28rem;width:fit-content;flex-wrap:wrap;border:1px solid var(--bd)}
.st{padding:.4rem .9rem;border-radius:9px;border:none;background:transparent;color:var(--tx3);font-size:.78rem;font-weight:600;transition:var(--tr);cursor:pointer}
.st:hover{color:var(--tx2)}
.st.on{background:var(--sr);color:var(--tx);box-shadow:var(--sh);border:1px solid var(--bd)}

/* ══ MODAL ══ */
.mbg{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;display:none;align-items:center;justify-content:center;padding:1rem;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.mbg.on{display:flex;animation:in .2s ease}
.modal{background:var(--sr);border:1px solid var(--glass-bd);border-radius:var(--r4);width:100%;max-width:500px;max-height:90vh;overflow-y:auto;padding:2rem;box-shadow:var(--sh3),var(--sh-glow);animation:slide-in .3s cubic-bezier(.4,0,.2,1);backdrop-filter:blur(40px)}
.mhdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem}
.mtitle{font-size:1.15rem;font-weight:800;letter-spacing:-.02em}
.mclose{width:32px;height:32px;border-radius:10px;background:var(--glass);border:1px solid var(--bd);display:flex;align-items:center;justify-content:center;color:var(--tx2);font-size:.9rem;cursor:pointer;transition:var(--tr)}
.mclose:hover{background:rgba(248,113,113,.08);color:var(--red);border-color:rgba(248,113,113,.2);transform:rotate(90deg)}

/* ══ CHAPTER TILE ══ */
.cht{background:var(--sr2);border:1px solid var(--bd);border-radius:14px;padding:1rem;cursor:pointer;transition:var(--tr);user-select:none;backdrop-filter:blur(8px)}
.cht:hover{border-color:var(--bd2);transform:translateY(-2px);box-shadow:var(--sh)}
.cht.exp{border-color:var(--acc);background:rgba(129,140,248,.05);box-shadow:0 0 0 3px rgba(129,140,248,.08),var(--sh)}

/* ══ SUBTOPIC ROW ══ */
.subrow{display:flex;align-items:center;gap:.6rem;padding:.55rem .8rem;border-radius:11px;cursor:pointer;border:1px solid var(--bd);background:var(--bg1);transition:var(--tr)}
.subrow:hover{border-color:var(--bd2);background:var(--sr);transform:translateX(3px)}
.subrow.on{background:rgba(129,140,248,.06);border-color:rgba(129,140,248,.2)}
.chk{width:18px;height:18px;flex-shrink:0;border-radius:5px;border:1.5px solid var(--bd2);display:flex;align-items:center;justify-content:center;transition:var(--tr-spring)}
.chk.on{background:linear-gradient(135deg,var(--acc),var(--acc2));border-color:transparent;box-shadow:0 2px 8px rgba(129,140,248,.3);transform:scale(1.05)}

/* ══ TABLE ══ */
.tbl{width:100%;border-collapse:collapse;font-size:.8rem}
.tbl th{text-align:left;padding:.6rem .8rem;font-size:.68rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--tx3);border-bottom:1px solid var(--bd)}
.tbl td{padding:.65rem .8rem;border-bottom:1px solid var(--bd);transition:var(--tr)}
.tbl tr:last-child td{border-bottom:none}
.tbl tr:hover td{background:rgba(129,140,248,.03)}
.tbl-w{overflow-x:auto}

/* ══ TIMER ══ */
.tw{position:relative;width:230px;height:230px}
.tsvg{position:absolute;top:0;left:0;transform:rotate(-90deg)}
.tc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.td{font-family:var(--m);font-size:2.4rem;font-weight:600;background:linear-gradient(135deg,var(--acc),var(--acc3));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:.02em}
.tl{font-size:.62rem;font-weight:700;color:var(--tx3);letter-spacing:.14em;text-transform:uppercase;margin-top:.3rem}

/* ══ CALENDAR ══ */
.cc{border-radius:10px;height:48px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;cursor:pointer;transition:var(--tr);border:1px solid var(--bd);background:var(--sr2)}
.cc:hover{border-color:var(--acc);background:rgba(129,140,248,.05);transform:scale(1.05)}
.cc input{width:90%;background:transparent;border:none;outline:none;text-align:center;font-family:var(--m);font-size:.7rem;color:var(--acc);font-weight:600}

/* ══ DOUBT ══ */
.dcard{background:var(--sr);border:1px solid var(--bd);border-radius:16px;padding:1.15rem;transition:var(--tr);cursor:pointer;backdrop-filter:blur(8px)}
.dcard:hover{border-color:var(--bd2);box-shadow:var(--sh2);transform:translateY(-2px)}
.dcard.solved{border-left:3px solid var(--grn)}
.drep{background:var(--bg1);border:1px solid var(--bd);border-radius:12px;padding:.95rem;margin-top:.7rem}

/* ══ LEADERBOARD ══ */
.lbr{display:flex;align-items:center;gap:.75rem;padding:.75rem;border-radius:12px;background:var(--sr2);border:1px solid var(--bd);transition:var(--tr);backdrop-filter:blur(8px)}
.lbr:hover{border-color:var(--bd2);background:var(--sr);transform:translateX(3px)}
.lbr.me{border-color:rgba(129,140,248,.3);background:rgba(129,140,248,.05);box-shadow:0 0 20px rgba(129,140,248,.08)}
.lba{width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,var(--acc),var(--acc3));display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;box-shadow:0 2px 8px rgba(129,140,248,.2)}

/* ══ ACTIVITY ══ */
.act{display:flex;gap:.75rem;padding:.65rem 0;border-bottom:1px solid var(--bd)}
.act:last-child{border-bottom:none}
.adot{width:8px;height:8px;border-radius:50%;background:linear-gradient(135deg,var(--acc),var(--acc2));flex-shrink:0;margin-top:.35rem;box-shadow:0 0 8px rgba(129,140,248,.3)}

/* ══ PRIORITY ══ */
.pi{display:flex;align-items:center;gap:.75rem;padding:.75rem;border-radius:12px;background:var(--sr2);border:1px solid var(--bd);transition:var(--tr);cursor:grab}
.pi:active{cursor:grabbing;opacity:.7;transform:scale(.98)}
.pi.dov{border-color:var(--acc);background:rgba(129,140,248,.06)}

/* ══ TOGGLE ══ */
.tgl{width:44px;height:24px;border-radius:99px;background:var(--bd2);border:none;position:relative;cursor:pointer;transition:var(--tr-smooth);flex-shrink:0}
.tgl.on{background:linear-gradient(135deg,var(--acc),var(--acc2));box-shadow:0 0 12px rgba(129,140,248,.25)}
.tgl::after{content:'';position:absolute;width:18px;height:18px;border-radius:50%;background:#fff;top:3px;left:3px;transition:var(--tr-spring);box-shadow:0 1px 4px rgba(0,0,0,.2)}
.tgl.on::after{left:23px}

/* ══ SETTING ROW ══ */
.srow{display:flex;justify-content:space-between;align-items:center;padding:.9rem 0;border-bottom:1px solid var(--bd)}
.srow:last-child{border-bottom:none}

/* ══ PROFILE HERO ══ */
.phero{background:linear-gradient(135deg,rgba(129,140,248,.1),rgba(192,132,252,.06));border:1px solid var(--bd);border-radius:var(--r4);padding:2rem;margin-bottom:1.2rem;position:relative;overflow:hidden;backdrop-filter:blur(20px)}
.phero::before{content:'';position:absolute;top:-50%;right:-20%;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(129,140,248,.08),transparent 70%);pointer-events:none}
.pav{width:72px;height:72px;border-radius:20px;background:linear-gradient(135deg,var(--acc),var(--acc3));display:flex;align-items:center;justify-content:center;font-size:2.1rem;box-shadow:0 8px 24px rgba(129,140,248,.3);position:relative}
.pav::after{content:'';position:absolute;inset:-3px;border-radius:23px;border:2px solid rgba(129,140,248,.2)}

/* ══ TOAST ══ */
.toast{position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;display:flex;align-items:center;gap:.65rem;padding:.75rem 1.1rem;background:var(--sr);border:1px solid var(--glass-bd);border-radius:14px;box-shadow:var(--sh3);font-size:.82rem;font-weight:500;animation:slide-in .3s ease;max-width:340px;pointer-events:none;backdrop-filter:blur(20px)}
.toast.ok{border-left:3px solid var(--grn)}
.toast.err{border-left:3px solid var(--red)}
.toast.warn{border-left:3px solid var(--yel);border-color:rgba(251,191,36,.15);background:rgba(251,191,36,.06);color:var(--yel)}

/* ══ CONFIRM DIALOG ══ */
.confirm-bg{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:9000;display:flex;align-items:center;justify-content:center;padding:1rem;backdrop-filter:blur(8px);animation:in .15s ease}
.confirm-box{background:var(--sr);border:1px solid var(--glass-bd);border-radius:var(--r4);width:100%;max-width:400px;padding:2rem;box-shadow:var(--sh3),var(--sh-glow);animation:slide-in .25s cubic-bezier(.4,0,.2,1);backdrop-filter:blur(40px)}
.confirm-icon{width:52px;height:52px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:1.6rem;margin:0 auto 1rem}
.confirm-icon.warn{background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.2)}
.confirm-icon.danger{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.2)}
.confirm-title{font-size:1.1rem;font-weight:800;text-align:center;margin-bottom:.45rem;letter-spacing:-.02em}
.confirm-msg{font-size:.82rem;color:var(--tx2);text-align:center;line-height:1.6;margin-bottom:1.35rem}
.confirm-input{width:100%;padding:.62rem .9rem;background:var(--bg1);border:1.5px solid var(--bd);border-radius:12px;color:var(--tx);font-size:.88rem;outline:none;transition:var(--tr);margin-bottom:1.1rem}
.confirm-input:focus{border-color:var(--acc);box-shadow:0 0 0 3px rgba(129,140,248,.12)}
.confirm-btns{display:flex;gap:.6rem}
.confirm-btns .btn{flex:1;justify-content:center;padding:.6rem 1rem}

/* ══ CHART ══ */
.cw{position:relative;height:190px;display:flex;align-items:flex-end;gap:.7rem;padding-top:1rem}
.bg{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;height:100%;justify-content:flex-end}
.bt2{display:flex;gap:2px;align-items:flex-end;height:100%;justify-content:center;width:100%}
.bc{border-radius:4px 4px 0 0;max-width:14px;flex:1;transition:height .6s cubic-bezier(.34,1.56,.64,1)}
.gl{position:absolute;left:0;right:0;border-top:1px dashed var(--bd);display:flex;align-items:center}

/* ══ SECTION HEADER ══ */
.sh{font-size:1.5rem;font-weight:800;color:var(--tx);letter-spacing:-.03em;background:linear-gradient(135deg,var(--tx),var(--tx2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.ss{font-size:.8rem;color:var(--tx3);margin-top:.25rem;font-weight:400}
.lbl{font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3)}

/* ══ RESPONSIVE ══ */
@media(max-width:1100px){.g-3{grid-template-columns:1fr 1fr}}
@media(max-width:768px){
  .g-3{grid-template-columns:1fr}.g-kpi{grid-template-columns:repeat(2,1fr)}
  .wrap{padding:0 .85rem}.hpills{display:none}.fr{grid-template-columns:1fr}
  .kv{font-size:1.7rem}
  .modal{padding:1.5rem;max-width:calc(100vw - 1.5rem);border-radius:20px}
  .confirm-box{padding:1.5rem;max-width:calc(100vw - 1.5rem)}
  header{height:52px}.hdr{height:52px}
  .brand-name{font-size:.95rem}.brand-icon{width:30px;height:30px;font-size:.85rem}
  .dd{right:-1rem;min-width:210px}
  .wn{right:-1rem;width:calc(100vw - 2rem);max-width:320px}
  nav{-webkit-overflow-scrolling:touch}
  .nav-inner{gap:0}
  .nb{padding:0 .8rem;font-size:.76rem}
  .card{padding:1.1rem;border-radius:14px}.flat{padding:1.1rem;border-radius:14px}
  .g-2{grid-template-columns:1fr}
  .g-plan{grid-template-columns:1fr}
  .toast{bottom:.75rem;right:.75rem;left:.75rem;max-width:none;border-radius:12px}
}
@media(max-width:540px){
  .g-kpi{grid-template-columns:1fr}.g-cal{grid-template-columns:repeat(7,1fr)}
  main{padding:.85rem 0}
  .wrap{padding:0 .65rem}
  .auth-card{padding:1.75rem;max-width:100%;border-radius:20px}
  .g-ch{grid-template-columns:repeat(auto-fill,minmax(125px,1fr))}
  .g-a{grid-template-columns:repeat(auto-fill,minmax(165px,1fr))}
  .g-sub{grid-template-columns:1fr}
  .card-hdr{flex-direction:column;align-items:flex-start;gap:.5rem}
  .btn{font-size:.76rem;padding:.44rem .78rem}
  .kv{font-size:1.5rem}
  .modal{padding:1.25rem;border-radius:16px}
  .mhdr{margin-bottom:1.1rem}
  .mtitle{font-size:1rem}
  .sh{font-size:1.2rem}
}
@media(max-width:400px){
  .auth-card{padding:1.35rem;border-radius:16px}.nb{padding:0 .55rem;font-size:.7rem}
  #exam-grid{grid-template-columns:repeat(2,1fr)!important}
  .brand-name{font-size:.85rem}
  html{font-size:14px}
  .confirm-box{padding:1.25rem;border-radius:16px}
  .confirm-title{font-size:.95rem}
}
.exam-opt{display:flex;flex-direction:column;align-items:center;gap:.3rem;padding:.6rem .35rem;border-radius:12px;border:1.5px solid var(--bd);cursor:pointer;transition:var(--tr-spring);background:var(--sr2);font-size:.68rem;font-weight:600;color:var(--tx3);text-align:center;backdrop-filter:blur(8px)}
.exam-opt:hover{border-color:var(--acc);background:rgba(129,140,248,.05);transform:translateY(-2px)}
.exam-opt.on{border-color:var(--acc);background:rgba(129,140,248,.1);color:var(--tx);box-shadow:0 0 0 2px rgba(129,140,248,.2),0 4px 12px rgba(129,140,248,.1)}
.exam-opt .exam-ico{font-size:1.35rem;line-height:1}
</style>
</head>
<body>

<!-- ═══ AUTH ═══ -->
<div id="auth">
  <div class="auth-orb auth-orb-1"></div>
  <div class="auth-orb auth-orb-2"></div>
  <div class="auth-orb auth-orb-3"></div>
  <div class="auth-card up" style="max-width:460px">
    <div class="auth-logo">
      <div class="auth-icon" id="auth-icon">⚡</div>
      <div class="auth-brand"><span id="auth-brand">Study</span><span>OS</span></div>
      <div class="auth-tagline" id="auth-tagline">Multi-Exam Study Platform</div>
    </div>
    <div class="auth-tabs">
      <button class="auth-tab on" onclick="atab('login')">Sign In</button>
      <button class="auth-tab" onclick="atab('reg')">Create Account</button>
    </div>
    <div class="auth-err" id="aerr"></div>

    <div id="lf">
      <div class="fg"><label class="fl">Username or Email</label><input class="fi" id="lu" type="text" placeholder="Enter username or email" autocomplete="username" onkeydown="if(event.key==='Enter')doLogin()"/></div>
      <div class="fg"><label class="fl">Password</label><input class="fi" id="lp" type="password" placeholder="Password" autocomplete="current-password" onkeydown="if(event.key==='Enter')doLogin()"/></div>
      <button class="auth-btn" onclick="doLogin()">Sign In →</button>
    </div>

    <div id="rf" class="hide">
      <div class="fg"><label class="fl">Choose Your Exam</label>
        <div id="exam-grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:.45rem;margin-top:.35rem"></div>
      </div>
      <div class="fr">
        <div class="fg"><label class="fl">Username</label><input class="fi" id="ru" type="text" placeholder="@handle" autocomplete="username"/></div>
        <div class="fg"><label class="fl">Display Name</label><input class="fi" id="rn" type="text" placeholder="Your name"/></div>
      </div>
      <div class="fg"><label class="fl">Email</label><input class="fi" id="re" type="email" placeholder="you@email.com"/></div>
      <div class="fr">
        <div class="fg"><label class="fl">Password</label><input class="fi" id="rp" type="password" placeholder="Min 6 chars"/></div>
        <div class="fg"><label class="fl">Confirm</label><input class="fi" id="rp2" type="password" placeholder="Repeat"/></div>
      </div>
      <div class="fg"><label class="fl">Pick Avatar</label><div class="emo-grid" id="aeg"></div></div>
      <button class="auth-btn" onclick="doReg()">Create Account →</button>
    </div>
  </div>
</div>

<!-- ═══ APP ═══ -->
<div id="app" class="hide">

  <!-- HEADER -->
  <header>
    <div class="wrap hdr">
      <div class="brand">
        <div class="brand-icon" id="b-icon">⚡</div>
        <div class="brand-name"><span id="b-name">Study</span><span>OS</span></div>
      </div>
      <div class="hpills" id="hpills">
        <div class="hp" id="h-streak" style="background:rgba(249,115,22,.1);border-color:rgba(249,115,22,.3);color:#f97316">🔥 0d</div>
        <div class="hp" id="h-hours"  style="background:rgba(99,102,241,.1);border-color:rgba(99,102,241,.3);color:#6366f1">⏱ 0h</div>
        <div class="hp" id="h-pct"    style="background:rgba(139,92,246,.1);border-color:rgba(139,92,246,.3);color:#8b5cf6">🎯 —</div>
      </div>
      <div class="hright">
        <!-- What's New -->
        <div style="position:relative">
          <div class="ibtn" onclick="toggleWN()" title="What's New">📣</div>
          <div class="wn" id="wn">
            <div class="wn-hdr">📣 What's New</div>
            <div id="wn-list"></div>
          </div>
        </div>
        <!-- Friends notif -->
        <div class="ibtn" onclick="go('friends')" title="Friends">👥<span class="bdg hide" id="fbdg"></span></div>
        <!-- Theme -->
        <div class="ibtn" id="thbtn" onclick="toggleTheme()" title="Toggle theme">🌙</div>
        <!-- Profile dropdown -->
        <div style="position:relative">
          <div class="av" id="avbtn" onclick="toggleDD()">?</div>
          <div class="dd" id="pdd">
            <div class="dd-hdr">
              <div class="dd-name" id="dd-name">—</div>
              <div class="dd-email" id="dd-email">—</div>
            </div>
            <div class="dd-item" onclick="openProfile();closeDD()">✏️ Edit Profile</div>
            <div class="dd-item" onclick="openSettings();closeDD()">⚙️ Settings</div>
            <div class="dd-item" onclick="go('activity');closeDD()">📋 Activity Log</div>
            <div class="dd-item" onclick="dlReport();closeDD()">📄 Download Report</div>
            <div class="dd-sep"></div>
            <div class="dd-item red" onclick="doLogout()">🚪 Sign Out</div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- NAV -->
  <nav>
    <div class="wrap nav-inner">
      <button class="nb on" data-t="dash" onclick="go('dash')">◈ Overview</button>
      <button class="nb" data-t="plan" onclick="go('plan')">◷ Study Plan</button>
      <button class="nb" data-t="heat" onclick="go('heat')">◫ Heatmap</button>
      <button class="nb" data-t="analytics" onclick="go('analytics')">◉ Analytics</button>
      <button class="nb" data-t="timer" onclick="go('timer')">◌ Focus</button>
      <button class="nb" data-t="mock" onclick="go('mock')">◆ Mock Tests</button>
      <button class="nb" data-t="doubts" onclick="go('doubts')">❓ Doubts</button>
      <button class="nb" data-t="friends" onclick="go('friends')">👥 Friends</button>
      <button class="nb" data-t="activity" onclick="go('activity')">📋 Activity</button>
    </div>
  </nav>

  <!-- MAIN -->
  <main>
   <div class="wrap">

    <!-- DASHBOARD -->
    <div id="t-dash" class="up">
      <div class="g-kpi mb-m" id="kpi"></div>
      <div class="g-3 mb-m" id="subm"></div>
      <div class="flat">
        <div class="card-hdr">
          <div><div class="lbl mb-s">Priority Queue</div><div class="ss">Your personal study focus list</div></div>
          <div class="flex gap-s">
            <button class="btn bo bsm" onclick="openMod('pm')">✏️ Customize</button>
            <button class="btn bo bsm" onclick="aiPrio()">🤖 AI Select</button>
          </div>
        </div>
        <div class="g-a" id="pdisp"></div>
      </div>
    </div>

    <!-- PLAN -->
    <div id="t-plan" class="up hide">
      <div class="flex btwn ctr wrap-f gap-m mb-m">
        <div><div class="sh">Today's Study Plan</div><div class="ss">Generated from your priority queue</div></div>
        <div class="flex gap-s">
          <input class="inp inp-sm" id="lhi" type="number" min="0" max="24" step=".5" placeholder="Hours" style="width:85px"/>
          <button class="btn bf" onclick="logH()">Log Hours</button>
        </div>
      </div>
      <div class="g-plan mb-m" id="pgrid"></div>
      <div class="flat">
        <div class="lbl mb-s">Spaced Repetition Schedule</div>
        <div class="ss mb-m">&lt;40% → Daily · 40-60% → Every 3 days · 60-80% → Weekly · >80% → Fortnightly</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.9rem" id="srgrid"></div>
      </div>
    </div>

    <!-- HEATMAP -->
    <div id="t-heat" class="up hide">
      <div class="sh mb-s">Topic Strength Heatmap</div>
      <div class="ss mb-m">Check subtopics — mastery auto-calculates</div>
      <div class="flex gap-s wrap-f mb-m" style="font-size:.72rem;color:var(--tx3);align-items:center">
        Legend:
        <span style="display:flex;align-items:center;gap:.25rem"><span style="width:9px;height:9px;border-radius:50%;background:#3a3f62;display:inline-block"></span>Not started</span>
        <span style="display:flex;align-items:center;gap:.25rem"><span style="width:9px;height:9px;border-radius:50%;background:#ef4444;display:inline-block"></span>Weak</span>
        <span style="display:flex;align-items:center;gap:.25rem"><span style="width:9px;height:9px;border-radius:50%;background:#f59e0b;display:inline-block"></span>Average</span>
        <span style="display:flex;align-items:center;gap:.25rem"><span style="width:9px;height:9px;border-radius:50%;background:#10b981;display:inline-block"></span>Strong</span>
      </div>
      <div class="stabs mb-m" id="stabs"></div>
      <div class="g-ch mb-m" id="chtiles"></div>
      <div id="expanel"></div>
    </div>

    <!-- ANALYTICS -->
    <div id="t-analytics" class="up hide">
      <div class="sh mb-s">Performance Analytics</div>
      <div class="ss mb-m">Your real data — nothing prefilled</div>
      <div id="anc"></div>
    </div>

    <!-- TIMER -->
    <div id="t-timer" class="up hide" style="display:flex;flex-direction:column;align-items:center;gap:1.65rem;max-width:480px;margin:0 auto">
      <div style="text-align:center"><div class="sh">Focus Timer</div><div class="ss">Sessions logged automatically</div></div>
      <div class="stabs" id="tmodes">
        <button class="st on" onclick="setMode('p',1500)">🍅 Pomodoro · 25m</button>
        <button class="st" onclick="setMode('d',5400)">🧠 Deep · 90m</button>
        <button class="st" onclick="setMode('b',2700)">⚡ Blitz · 45m</button>
      </div>
      <div class="tw">
        <svg class="tsvg" width="230" height="230">
          <circle cx="115" cy="115" r="100" fill="none" stroke="var(--bd)" stroke-width="3"/>
          <circle id="tring" cx="115" cy="115" r="100" fill="none" stroke="var(--phy)" stroke-width="3"
            stroke-dasharray="628.3" stroke-dashoffset="628.3" stroke-linecap="round"
            style="transition:stroke-dashoffset 1s linear;opacity:.25"/>
        </svg>
        <div class="tc">
          <div class="td" id="tdisp">00:00:00</div>
          <div class="tl" id="tstat">READY</div>
        </div>
      </div>
      <div class="flex gap-s">
        <button class="btn bf bw" id="tstrt" onclick="toggleTimer()">▶ Start</button>
        <button class="btn bd2 bw" onclick="stopTimer()">⏹ Stop & Log</button>
      </div>
      <div class="card full" id="sescard" style="display:none">
        <div class="lbl mb-m">Today's Sessions</div>
        <div id="seslist"></div>
        <div class="flex btwn mt-s"><span style="font-weight:700;font-size:.85rem">Total</span><span style="font-family:var(--m);font-size:.88rem;color:var(--phy);font-weight:600" id="sestot">00:00:00</span></div>
      </div>
    </div>

    <!-- MOCK TESTS -->
    <div id="t-mock" class="up hide">
      <div class="sh mb-s">Mock Test Tracker</div>
      <div class="ss mb-m">Log scores, get instant AI percentile prediction</div>
      <div class="card mb-m">
        <div class="lbl mb-m">Add New Test</div>
        <div class="flex gap-m wrap-f mb-m" id="mock-inputs"></div>
        <div id="prevbox" style="display:none;background:var(--bg1);border:1.5px solid var(--bd);border-radius:var(--r);padding:.85rem 1rem;margin-bottom:.8rem;align-items:center;gap:1rem">
          <div><div class="lbl">Predicted</div><div style="font-size:1.85rem;font-weight:800;color:var(--pri,#8b5cf6);line-height:1;letter-spacing:-.02em"><span id="ppct">—</span><span style="font-size:.85rem">%ile</span></div></div>
          <span id="pbadge" class="chip"></span>
        </div>
        <button class="btn bf" onclick="addTest()">Add Test Result</button>
      </div>
      <div class="flat">
        <div class="card-hdr">
          <div class="lbl">Test History <span id="tcnt" style="color:var(--tx3);font-weight:400;text-transform:none;letter-spacing:0;font-size:.78rem"></span></div>
          <div id="clrrow"></div>
        </div>
        <div id="thist"></div>
      </div>
    </div>

    <!-- DOUBTS -->
    <div id="t-doubts" class="up hide">
      <div class="flex btwn ctr wrap-f gap-m mb-m">
        <div><div class="sh">Doubts Community</div><div class="ss">Post doubts, get answers from classmates</div></div>
        <button class="btn bf" onclick="openMod('pdm')">+ Post Doubt</button>
      </div>
      <div class="flex gap-s mb-m wrap-f" id="doubt-tabs">
        <button class="st on" onclick="loadDoubts('All')">All</button>
        <button class="st" onclick="loadDoubts('General')">General</button>
      </div>
      <div id="dlist" class="fc gap-s"></div>
    </div>

    <!-- FRIENDS -->
    <div id="t-friends" class="up hide">
      <div class="flex btwn ctr wrap-f gap-m mb-m">
        <div><div class="sh">Friends & Leaderboard</div><div class="ss">Compete on percentile, hours & mastery</div></div>
        <button class="btn bf" onclick="openMod('afm')">+ Add Friend</button>
      </div>
      <div id="preqs" class="mb-m hide"><div class="lbl mb-s">Pending Requests</div><div id="preqlist" class="fc gap-s"></div></div>
      <div class="lbl mb-s">Leaderboard</div>
      <div id="lboard" class="fc gap-s"></div>
    </div>

    <!-- ACTIVITY -->
    <div id="t-activity" class="up hide">
      <div class="sh mb-m">Activity Log</div>
      <div class="flat"><div id="actlist"></div></div>
    </div>

   </div>
  </main>
</div>

<!-- ═══ MODALS ═══ -->

<!-- Profile modal -->
<div class="mbg" id="pm2"><div class="modal up">
  <div class="mhdr"><div class="mtitle">Edit Profile</div><div class="mclose" onclick="closeMod('pm2')">✕</div></div>
  <div class="fg"><label class="fl">Display Name</label><input class="fi" id="pn" type="text"/></div>
  <div class="fg"><label class="fl">Bio</label><textarea class="fi" id="pb" rows="2" placeholder="Tell others about yourself..."></textarea></div>
  <div class="fr"><div class="fg"><label class="fl">Target College</label><input class="fi" id="pc" type="text" placeholder="YOUR DREAM COLLEGE/UNI"/></div>
  <div class="fg"><label class="fl">Exam Date</label><input class="fi" id="pe" type="date"/></div></div>
  <div class="fg"><label class="fl">Avatar</label><div class="emo-grid" id="peg"></div></div>
  <div style="margin-top:1.35rem;padding-top:1.1rem;border-top:1.5px solid var(--bd)">
    <div class="lbl mb-m">Change Exam</div>
    <div class="fg"><label class="fl">Switch to a different exam (your topic progress will be preserved, new topics will be added)</label>
      <select class="fi" id="pexam" onchange="switchExam(this.value)"></select>
    </div>
  </div>
  <div style="margin-top:1.35rem;padding-top:1.1rem;border-top:1.5px solid var(--bd)">
    <div class="lbl mb-m">Change Password</div>
    <div class="fg"><label class="fl">Current Password</label><input class="fi" id="op" type="password" placeholder="Current password"/></div>
    <div class="fr"><div class="fg"><label class="fl">New Password</label><input class="fi" id="np" type="password" placeholder="Min 6 chars"/></div>
    <div class="fg"><label class="fl">Confirm New</label><input class="fi" id="np2" type="password" placeholder="Repeat"/></div></div>
  </div>
  <div class="flex gap-s mt-m"><button class="btn bf" style="flex:1" onclick="saveProf()">Save Changes</button><button class="btn bo" onclick="closeMod('pm2')">Cancel</button></div>
</div></div>

<!-- Settings modal -->
<div class="mbg" id="sm"><div class="modal up">
  <div class="mhdr"><div class="mtitle">Settings</div><div class="mclose" onclick="closeMod('sm')">✕</div></div>
  <div class="srow"><div><div style="font-weight:600;font-size:.88rem">Dark Mode</div><div style="font-size:.75rem;color:var(--tx3);margin-top:.12rem">Toggle between dark and light theme</div></div><button class="tgl on" id="thtgl" onclick="toggleTheme()"></button></div>
  <div class="srow"><div><div style="font-weight:600;font-size:.88rem">Notifications</div><div style="font-size:.75rem;color:var(--tx3);margin-top:.12rem">Friend requests and replies</div></div><button class="tgl on"></button></div>
  <div class="srow"><div><div style="font-weight:600;font-size:.88rem">Timer Sound</div><div style="font-size:.75rem;color:var(--tx3);margin-top:.12rem">Play sound when timer ends</div></div><button class="tgl"></button></div>
  <div style="margin-top:1.25rem;padding-top:1rem;border-top:1.5px solid var(--bd)">
    <div class="lbl mb-m">Danger Zone</div>
    <button class="btn bd2 full" onclick="deleteAccount()">Delete My Account</button>
  </div>
</div></div>

<!-- Priority modal -->
<div class="mbg" id="pm"><div class="modal up" style="max-width:600px">
  <div class="mhdr"><div class="mtitle">Customize Priority Queue</div><div class="mclose" onclick="closeMod('pm')">✕</div></div>
  <div class="ss mb-m">Drag to reorder · Click × to remove · Topics studied in this order</div>
  <div class="flex gap-s mb-m">
    <select class="inp inp-sm" id="pasub" style="flex:1" onchange="buildTopicDd(this.value)">
      <option value="">Subject...</option>
    </select>
    <select class="inp inp-sm" id="patop" style="flex:2"><option value="">Select topic...</option></select>
    <button class="btn bf bsm" onclick="addPrio()">+ Add</button>
  </div>
  <div id="plist" class="fc gap-s" style="max-height:320px;overflow-y:auto"></div>
  <div class="flex gap-s mt-m">
    <button class="btn bf" style="flex:1" onclick="savePrio()">Save List</button>
    <button class="btn bo bsm" onclick="aiPrio();closeMod('pm')">🤖 AI Auto-Select</button>
  </div>
</div></div>

<!-- Add Friend -->
<div class="mbg" id="afm"><div class="modal up" style="max-width:360px">
  <div class="mhdr"><div class="mtitle">Add Friend</div><div class="mclose" onclick="closeMod('afm')">✕</div></div>
  <div class="fg"><label class="fl">Username</label><input class="fi" id="fui" type="text" placeholder="@username" onkeydown="if(event.key==='Enter')addFriend()"/></div>
  <div id="ferr" style="color:var(--red);font-size:.8rem;margin-bottom:.5rem;display:none"></div>
  <button class="btn bf full" onclick="addFriend()">Send Friend Request</button>
</div></div>

<!-- Post Doubt -->
<div class="mbg" id="pdm"><div class="modal up" style="max-width:560px">
  <div class="mhdr"><div class="mtitle">Post a Doubt</div><div class="mclose" onclick="closeMod('pdm')">✕</div></div>
  <div class="fg"><label class="fl">Title</label><input class="fi" id="dtit" type="text" placeholder="Brief summary of your doubt"/></div>
  <div class="fr">
    <div class="fg"><label class="fl">Subject</label><select class="fi" id="dsub"><option>General</option></select></div>
    <div class="fg"><label class="fl">Attach</label><select class="fi" id="dtype"><option value="none">Text only</option><option value="image">Add Image</option></select></div>
  </div>
  <div class="fg"><label class="fl">Your Doubt</label><textarea class="fi" id="dbod" rows="4" placeholder="Describe your doubt in detail..."></textarea></div>
  <div id="dimgsec" style="display:none"><label class="fl">Image</label><input type="file" id="dimg" accept="image/*" class="fi" style="padding:.38rem"/></div>
  <button class="btn bf full mt-m" onclick="postDoubt()">Post Doubt</button>
</div></div>

<!-- Doubt Detail -->
<div class="mbg" id="ddm"><div class="modal up" style="max-width:620px;max-height:88vh;overflow-y:auto">
  <div class="mhdr"><div class="mtitle" id="ddtit">Doubt</div><div class="mclose" onclick="closeMod('ddm')">✕</div></div>
  <div id="ddcon"></div>
</div></div>

<script>
// ════════════════════════════════════════════════════════
// GLOBALS
// ════════════════════════════════════════════════════════
let S={}, ME=null, TAB='dash', ASUB='', EXP=null;
let PRIO=[], SEL_EMO='🎯', DRAG_I=null, SEL_EXAM='JEE';
let T_SEC=0, T_RUN=false, T_INT=null, T_MODE='p', T_MSEC=1500;
let SESS=[], TSEC_TOT=0;
let EDT_ID=null, CLR_CNF=false, CAL_ED=null;
let LB_CACHE={}, DF='All';
const AVTS=['🎯','🚀','🔥','⚡','🏆','💡','🦁','🐯','🦅','🎓','📚','🌟'];
let SC={}, SI={};
const EXAM_DATA={JEE:{icon:'⚡',name:'JEE'},NEET:{icon:'🩺',name:'NEET'},UPSC:{icon:'🏛️',name:'UPSC'},CAT:{icon:'📈',name:'CAT'},GATE:{icon:'💻',name:'GATE'},CLAT:{icon:'⚖️',name:'CLAT'},SSC:{icon:'🏢',name:'SSC'},Banking:{icon:'🏦',name:'Banking'}};

// ════════════════════════════════════════════════════════
// UTILS
// ════════════════════════════════════════════════════════
const api=(p,b)=>fetch(p,b?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}:{}).then(r=>r.json().catch(()=>({})));
const $=(s,r=document)=>r.querySelector(s);
const scColor=s=>s>=80?'#10b981':s>=60?'#84cc16':s>=40?'#f59e0b':s>=15?'#f97316':s>0?'#ef4444':'#3a3f62';
const fmtT=s=>[Math.floor(s/3600),Math.floor((s%3600)/60),s%60].map(x=>String(x).padStart(2,'0')).join(':');
function cpct(...vals){const v=vals.filter(x=>x!=null&&!isNaN(x));if(!v.length)return 0;const n=v.reduce((a,b)=>a+b,0)/v.length;if(n>=90)return+(99+(n-90)*.1).toFixed(1);if(n>=80)return+(95+(n-80)*.4).toFixed(1);if(n>=70)return+(88+(n-70)*.7).toFixed(1);if(n>=60)return+(78+(n-60)*1).toFixed(1);if(n>=50)return+(60+(n-50)*1.8).toFixed(1);return+Math.max(10,n*1.2).toFixed(1);}
function pinfo(p){const tiers=(S.exam||{}).tiers||[[99,'🏆 Top Rank'],[95,'⭐ Excellent'],[85,'✅ Good'],[0,'📈 Keep Pushing']];for(const[th,lbl]of tiers)if(p>=th)return[th>=99?'#f59e0b':th>=95?'#6366f1':th>=85?'#10b981':'#5a5f80',lbl];return['#5a5f80','📈 Keep Pushing'];}
const bar=(pct,col,h=5)=>`<div class="bt" style="height:${h}px"><div class="bf2" style="width:${Math.min(pct||0,100)}%;height:100%;background:linear-gradient(90deg,${col}99,${col})"></div></div>`;
const chip=(txt,col)=>`<span class="chip" style="color:${col};background:${col}15;border-color:${col}40">${txt}</span>`;
const today=()=>new Date().toISOString().split('T')[0];
const rel=s=>{if(!s)return'';const d=new Date(s.includes('T')?s:s.replace(' ','T')+'Z'),df=(Date.now()-d)/1000;return df<60?'just now':df<3600?`${~~(df/60)}m ago`:df<86400?`${~~(df/3600)}h ago`:`${~~(df/86400)}d ago`;};

function toast(msg,type='ok'){
  const e=document.createElement('div');e.className=`toast ${type}`;e.textContent=(type==='ok'?'✓ ':type==='warn'?'⚠ ':'✕ ')+msg;
  document.body.appendChild(e);setTimeout(()=>e.remove(),3000);
}
function siteConfirm({icon='⚠️',iconType='warn',title='Are you sure?',msg='',confirmText='Confirm',cancelText='Cancel',confirmClass='bf',inputPlaceholder='',inputType='text'}={}){
  return new Promise(resolve=>{
    const bg=document.createElement('div');bg.className='confirm-bg';
    bg.innerHTML=`<div class="confirm-box">
      <div class="confirm-icon ${iconType}">${icon}</div>
      <div class="confirm-title">${title}</div>
      <div class="confirm-msg">${msg}</div>
      ${inputPlaceholder?`<input class="confirm-input" type="${inputType}" placeholder="${inputPlaceholder}" autocomplete="off"/>`:'' }
      <div class="confirm-btns">
        <button class="btn bo" id="cf-no">${cancelText}</button>
        <button class="btn ${confirmClass}" id="cf-yes">${confirmText}</button>
      </div>
    </div>`;
    document.body.appendChild(bg);
    const inp=bg.querySelector('.confirm-input');
    if(inp)inp.focus();
    bg.querySelector('#cf-no').onclick=()=>{bg.remove();resolve(false);};
    bg.querySelector('#cf-yes').onclick=()=>{bg.remove();resolve(inp?inp.value:true);};
    bg.addEventListener('click',e=>{if(e.target===bg){bg.remove();resolve(false);}});
    document.addEventListener('keydown',function esc(e){if(e.key==='Escape'){bg.remove();resolve(false);document.removeEventListener('keydown',esc);}},{once:true});
  });
}
function openMod(id){document.getElementById(id).classList.add('on')}
function closeMod(id){document.getElementById(id).classList.remove('on')}
function closeDD(){document.querySelectorAll('.dd,.wn').forEach(d=>d.classList.remove('on'))}
document.addEventListener('click',e=>{if(!e.target.closest('.hright'))closeDD();});

// ════════════════════════════════════════════════════════
// AUTH
// ════════════════════════════════════════════════════════
function atab(t){
  [$('#lf'),$('#rf')].forEach((el,i)=>el.classList.toggle('hide',i!==(t==='login'?0:1)));
  document.querySelectorAll('.auth-tab').forEach((b,i)=>b.classList.toggle('on',i===(t==='login'?0:1)));
  $('#aerr').style.display='none';
}
function buildExamGrid(){
  const el=$('#exam-grid');if(!el)return;
  el.innerHTML=Object.entries(EXAM_DATA).map(([k,v])=>`<div class="exam-opt${SEL_EXAM===k?' on':''}" onclick="selExam('${k}')"><div class="exam-ico">${v.icon}</div>${v.name}</div>`).join('');
}
function selExam(k){
  SEL_EXAM=k;buildExamGrid();
  const d=EXAM_DATA[k]||{};
  $('#auth-icon').textContent=d.icon||'⚡';
  $('#auth-brand').textContent=k;
}
function buildEmoGrid(id,fn){
  const el=document.getElementById(id);if(!el)return;
  el.innerHTML=AVTS.map(e=>`<div class="emo-opt${e===SEL_EMO?' on':''}" onclick="${fn}('${e}')">${e}</div>`).join('');
}
function selEmo(e){SEL_EMO=e;buildEmoGrid('aeg','selEmo');}
function selPEmo(e){SEL_EMO=e;buildEmoGrid('peg','selPEmo');}

async function doLogin(){
  const e=$('#aerr');e.style.display='none';
  const r=await api('/api/login',{username:$('#lu').value.trim(),password:$('#lp').value});
  if(r.error){e.textContent=r.error;e.style.display='block';return;}
  await boot();
}
async function doReg(){
  const e=$('#aerr');e.style.display='none';
  const r=await api('/api/register',{username:$('#ru').value.trim(),name:$('#rn').value.trim(),email:$('#re').value.trim(),password:$('#rp').value,password2:$('#rp2').value,avatar:SEL_EMO,exam_type:SEL_EXAM});
  if(r.error){e.textContent=r.error;e.style.display='block';return;}
  await boot();
}
async function doLogout(){await api('/api/logout',{});location.reload();}

// ════════════════════════════════════════════════════════
// BOOT
// ════════════════════════════════════════════════════════
async function boot(){
  const st=await api('/api/state');
  if(st.error)return;
  S=st; ME=st.user;
  // Build dynamic subject maps from server data
  SC={}; SI={};
  const subs=st.subjects||{};
  Object.entries(subs).forEach(([name,info])=>{SC[name]=info.color;SI[name]=info.icon;});
  if(!ASUB||!SC[ASUB]) ASUB=Object.keys(SC)[0]||'';
  // Branding
  const ex=st.exam||{};
  $('#b-icon').textContent=ex.icon||'⚡';
  $('#b-name').textContent=ex.brand||'Study';
  document.title=(ex.brand||'Study')+'OS';
  PRIO=(st.priority||[]).map(k=>{const[sub,top]=k.split('::');return{key:k,subject:sub,topic:top,score:st.topic_scores[k]||0};});
  if(!PRIO.length) PRIO=(st.weak_topics||[]).slice(0,8).map(w=>({...w}));
  document.documentElement.setAttribute('data-theme',ME.theme||'dark');
  updateThemeUI();
  $('#dd-name').textContent=ME.name||ME.username;
  $('#dd-email').textContent=ME.email;
  $('#avbtn').textContent=ME.avatar||'🎯';
  $('#wn-list').innerHTML=(S.changelog||[]).map(([v,t,b])=>`<div class="wn-item"><div class="wn-ver">${v}</div><div class="wn-title">${t}</div><div class="wn-body">${b}</div></div>`).join('');
  const pn=(st.pending||[]).length;
  if(pn>0){$('#fbdg').textContent=pn;$('#fbdg').classList.remove('hide');}else $('#fbdg').classList.add('hide');
  // Populate dynamic dropdowns
  const subOpts=Object.keys(SC).map(s=>`<option>${s}</option>`).join('');
  const pa=$('#pasub');if(pa)pa.innerHTML=`<option value="">Subject...</option>`+subOpts;
  const ds=$('#dsub');if(ds)ds.innerHTML=`<option>General</option>`+subOpts;
  const dt=$('#doubt-tabs');if(dt)dt.innerHTML=`<button class="st on" onclick="loadDoubts('All')">All</button>`+Object.entries(SC).map(([s,c])=>`<button class="st" onclick="loadDoubts('${s}')">${SI[s]} ${s}</button>`).join('');
  // Build dynamic mock test inputs
  buildMockInputs();
  $('#idate').value=today();
  buildEmoGrid('aeg','selEmo');
  updateHdr();
  $('#auth').classList.add('gone');
  $('#app').classList.remove('hide');
  render('dash');
}
function buildMockInputs(){
  const c=$('#mock-inputs');if(!c)return;
  c.innerHTML=Object.entries(SC).map(([name,col])=>`<div style="flex:1;min-width:85px"><div class="lbl mb-s" style="color:${col}">${name} %</div><input class="inp inp-sm" data-sub="${name}" type="number" min="0" max="100" placeholder="0–100" oninput="prevTest()"/></div>`).join('')+`<div style="flex:1;min-width:105px"><div class="lbl mb-s">Date</div><input class="inp inp-sm" id="idate" type="date" value="${today()}"/></div>`;
}

function updateHdr(){
  const p=S.predicted_pct,th=S.study_log?.[today()]||0;
  $('#h-streak').innerHTML=`🔥 ${S.streak||0}d`;
  $('#h-hours').innerHTML=`⏱ ${th.toFixed(1)}h`;
  $('#h-pct').innerHTML=p?`🎯 ${p.toFixed(1)}%ile`:'🎯 —';
}

// ════════════════════════════════════════════════════════
// TAB ROUTING
// ════════════════════════════════════════════════════════
function go(t){
  document.querySelectorAll('.nb').forEach(b=>b.classList.toggle('on',b.dataset.t===t));
  document.querySelectorAll('main [id^="t-"]').forEach(d=>d.classList.toggle('hide',d.id!==`t-${t}`));
  TAB=t; render(t);
}
function render(t){
  if(t==='dash')     rDash();
  if(t==='plan')     rPlan();
  if(t==='heat')     rHeat();
  if(t==='analytics')rAn();
  if(t==='mock')     rMock();
  if(t==='doubts')   loadDoubts(DF);
  if(t==='friends')  rFriends();
  if(t==='activity') rActivity();
}

// ════════════════════════════════════════════════════════
// DASHBOARD
// ════════════════════════════════════════════════════════
function rDash(){
  const {topic_scores:sc,predicted_pct:pred,streak,total_hours:th}=S;
  const mastered=Object.values(sc).filter(v=>v===100).length,total=Object.keys(sc).length;
  const kpis=[
    {label:'Predicted Percentile',val:pred?pred.toFixed(1):'—',unit:pred?'%ile':'',color:'#8b5cf6',sub:pred?pinfo(pred)[1]:'Add a mock test'},
    {label:'Study Streak',val:streak||0,unit:' days',color:'#f97316',sub:(streak||0)>=7?'Week Warrior 🏆':(streak||0)>=3?'Building momentum':'Start the chain today'},
    {label:'Hours Logged',val:(th||0).toFixed(0),unit:'h',color:'#6366f1',sub:`${((th||0)/30).toFixed(1)}h avg/day (30d)`},
    {label:'Chapters Mastered',val:mastered,unit:`/${total}`,color:'#10b981',sub:`${((mastered/Math.max(total,1))*100).toFixed(0)}% complete`},
  ];
  $('#kpi').innerHTML=kpis.map(k=>`<div class="card kpi"><div class="lbl">${k.label}</div><div class="kv" style="color:${k.color}">${k.val}<span class="ku">${k.unit}</span></div><div class="ks">${k.sub}</div><div class="deco" style="background:${k.color}"></div></div>`).join('');
  $('#subm').innerHTML=Object.keys(SC).map(sub=>{
    const vals=Object.entries(sc).filter(([k])=>k.startsWith(sub)).map(([,v])=>v);
    const avg=vals.length?Math.round(vals.reduce((a,b)=>a+b,0)/vals.length):0;
    const c=SC[sub];
    return `<div class="card"><div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.9rem"><div><div class="lbl">${sub}</div><div style="font-size:1.9rem;font-weight:800;color:${c};line-height:1;margin-top:.3rem;letter-spacing:-.03em">${avg}<span style="font-size:.9rem">%</span></div></div><div style="width:42px;height:42px;border-radius:11px;background:${c}18;border:1.5px solid ${c}30;display:flex;align-items:center;justify-content:center;font-size:1.3rem">${SI[sub]}</div></div>${bar(avg,c,6)}<div style="font-size:.7rem;color:var(--tx3);margin-top:.45rem">${(S.subjects||{})[sub]?.topics?.length||12} chapters</div></div>`;
  }).join('');
  const disp=PRIO.length?PRIO:(S.weak_topics||[]).slice(0,8);
  $('#pdisp').innerHTML=disp.length?disp.map((item,i)=>{
    const c=SC[item.subject]||'#6366f1',sc2=scColor(item.score);
    return `<div style="background:var(--sr2);border:1.5px solid var(--bd);border-radius:var(--r2);padding:.85rem;display:flex;flex-direction:column;gap:.38rem"><div style="display:flex;justify-content:space-between;align-items:center">${chip(item.subject,c)}<span style="font-family:var(--m);font-size:.62rem;color:var(--tx3)">#${i+1}</span></div><div style="font-weight:700;font-size:.86rem;color:var(--tx)">${item.topic}</div><div style="display:flex;align-items:center;gap:.48rem"><div style="flex:1">${bar(item.score,sc2)}</div><span style="font-family:var(--m);font-size:.67rem;color:${sc2};font-weight:600">${item.score}%</span></div></div>`;
  }).join(''):`<p style="color:var(--tx3);font-size:.84rem">No topics yet — go to Heatmap to mark progress, or click AI Select.</p>`;
}

// ════════════════════════════════════════════════════════
// PRIORITY QUEUE
// ════════════════════════════════════════════════════════
function buildTopicDd(sub){
  const el=$('#patop');
  const tops=(S.subjects||{})[sub]?.topics||[];
  el.innerHTML=`<option value="">Select topic...</option>`+tops.map(t=>`<option value="${sub}::${t}">${t}</option>`).join('');
}
function buildPList(){
  $('#plist').innerHTML=PRIO.map((item,i)=>`<div class="pi" draggable="true" data-i="${i}" ondragstart="dStart(${i})" ondragover="dOver(event,${i})" ondrop="dDrop(${i})" ondragleave="dLeave(event)">
    <span style="color:var(--tx3);font-size:.78rem;font-family:var(--m);width:18px">${i+1}</span>
    <span style="font-size:.95rem">${SI[item.subject]||'?'}</span>
    <div style="flex:1"><div style="font-weight:600;font-size:.83rem">${item.topic}</div><div style="font-size:.7rem;color:var(--tx3)">${item.subject} · ${item.score}%</div></div>
    <button class="btn bd2 bxs" onclick="remPrio(${i})">✕</button>
  </div>`).join('');
}
function dStart(i){DRAG_I=i;}
function dOver(e,i){e.preventDefault();document.querySelectorAll('.pi').forEach((el,j)=>el.classList.toggle('dov',j===i));}
function dLeave(e){if(!e.currentTarget.contains(e.relatedTarget))e.currentTarget.classList.remove('dov');}
function dDrop(i){if(DRAG_I===null||DRAG_I===i)return;const[m]=PRIO.splice(DRAG_I,1);PRIO.splice(i,0,m);DRAG_I=null;document.querySelectorAll('.pi').forEach(el=>el.classList.remove('dov'));buildPList();}
function remPrio(i){PRIO.splice(i,1);buildPList();}
function addPrio(){
  const k=$('#patop').value;if(!k)return;
  if(PRIO.find(p=>p.key===k)){toast('Already in list','err');return;}
  const[sub,top]=k.split('::');
  PRIO.push({key:k,subject:sub,topic:top,score:S.topic_scores?.[k]||0});
  buildPList();$('#patop').value='';
}
async function savePrio(){
  await api('/api/set_priority',{keys:PRIO.map(p=>p.key)});
  S.priority=PRIO.map(p=>p.key);toast('Priority list saved');closeMod('pm');rDash();
}
function aiPrio(){
  PRIO=(S.weak_topics||[]).slice(0,8).map(w=>({...w}));
  api('/api/set_priority',{keys:PRIO.map(p=>p.key)});
  S.priority=PRIO.map(p=>p.key);toast('AI selected 8 weakest topics');rDash();
  if(document.getElementById('pm').classList.contains('on'))buildPList();
}
function openPrioMod(){buildPList();buildTopicDd($('#pasub').value);openMod('pm');}

// ════════════════════════════════════════════════════════
// STUDY PLAN
// ════════════════════════════════════════════════════════
function rPlan(){
  const{daily_plan:plan,topic_scores:sc}=S;
  if(!plan||!plan.length){$('#pgrid').innerHTML=`<div class="card" style="grid-column:1/-1;text-align:center;padding:2.75rem"><div style="font-size:1.85rem;margin-bottom:.65rem">📋</div><div style="font-weight:700;color:var(--tx2);margin-bottom:.35rem">No plan yet</div><div style="font-size:.8rem;color:var(--tx3)">Set your priority queue or mark topics in the Heatmap.</div></div>`;$('#srgrid').innerHTML='';return;}
  $('#pgrid').innerHTML=plan.map(item=>{
    const c=SC[item.subject]||'#6366f1',sc2=scColor(item.score);
    const note=item.score<40?'Revise from scratch → concepts + 30 PYQs':item.score<60?'PYQ pattern recognition mode':'Speed drills — timed practice sets';
    return `<div class="card" style="border-left:3px solid ${c}"><div style="display:flex;justify-content:space-between;margin-bottom:.7rem"><div style="display:flex;flex-direction:column;gap:.28rem"><span style="font-size:.68rem;font-family:var(--m);color:var(--tx3)">${item.time}</span>${chip(item.subject,c)}</div><div style="text-align:right"><div style="font-size:1.05rem;font-weight:700;color:${c};font-family:var(--m)">${item.hours.toFixed(1)}h</div><div style="font-size:.62rem;color:var(--tx3)">recommended</div></div></div><div style="font-weight:700;font-size:.95rem;margin-bottom:.6rem">${item.topic}</div><div style="display:flex;align-items:center;gap:.45rem;margin-bottom:.6rem"><div style="flex:1">${bar(item.score,sc2)}</div><span style="font-size:.68rem;color:${sc2};font-weight:600;font-family:var(--m)">${item.score}%</span></div><p style="font-size:.72rem;color:var(--tx3);font-style:italic;margin-bottom:.7rem">${note}</p><button class="btn bo bsm" onclick="boost('${item.key}')" style="border-color:${c}40;color:${c}">+ Mark Progress</button></div>`;
  }).join('');
  const sr=S.sr_schedule||{};
  const bkts=[['today','Today 🔴'],['3days','In 3 days 🟡'],['weekly','Weekly 🟢'],['fortnightly','Fortnightly ⚪']];
  $('#srgrid').innerHTML=bkts.map(([k,label])=>{
    const items=(sr[k]||[]).slice(0,5);
    return `<div><div style="font-size:.68rem;font-weight:700;color:var(--tx3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.45rem">${label}</div>${items.map(t=>{const c=SC[t.sub]||'#6366f1';return`<div style="font-size:.72rem;color:${c};padding:.24rem .52rem;background:${c}14;border-radius:6px;margin-bottom:.28rem;border:1.5px solid ${c}28;font-weight:500">${t.topic}</div>`;}).join('')||`<div style="font-size:.7rem;color:var(--tx3);font-style:italic">None</div>`}</div>`;
  }).join('');
}
async function logH(){
  const h=parseFloat($('#lhi').value);if(!h||h<=0)return;
  await api('/api/log_hours',{date:today(),hours:h});$('#lhi').value='';
  const d=today();if(!S.study_log)S.study_log={};S.study_log[d]=(S.study_log[d]||0)+h;
  updateHdr();toast(`Logged ${h}h for today`);
}
async function boost(key){
  const r=await api('/api/boost',{key,delta:5});
  if(S.topic_scores)S.topic_scores[key]=r.score;
  const p=PRIO.find(p=>p.key===key);if(p)p.score=r.score;
  toast(`+5% on ${key.split('::')[1]}`);rDash();
}

// ════════════════════════════════════════════════════════
// HEATMAP
// ════════════════════════════════════════════════════════
function rHeat(){
  const subs=S.subtopics||{},scores=S.topic_scores||{},chk=S.checked||{};
  $('#stabs').innerHTML=Object.keys(SC).map(sub=>{
    const vals=Object.entries(scores).filter(([k])=>k.startsWith(sub)).map(([,v])=>v);
    const avg=vals.length?Math.round(vals.reduce((a,b)=>a+b,0)/vals.length):0;
    return `<button class="st${ASUB===sub?' on':''}" onclick="switchSub('${sub}')" style="${ASUB===sub?`color:${SC[sub]}`:''}">
      ${SI[sub]} ${sub} <span style="font-size:.66rem;opacity:.6;font-family:var(--m)">${avg}%</span></button>`;
  }).join('');
  const c=SC[ASUB]||'#6366f1';
  const tops=(S.subjects||{})[ASUB]?.topics||[];
  $('#chtiles').innerHTML=tops.map(ch=>{
    const key=`${ASUB}::${ch}`,score=scores[key]||0,c2=score?scColor(score):scColor(0);
    const all=subs[key]||[],done=all.filter(s=>chk[`${key}::${s}`]).length;
    const ex=EXP===key;
    return `<div class="cht${ex?' exp':''}" onclick="togCh('${key}')"><div style="font-size:.7rem;color:var(--tx3);margin-bottom:.38rem;font-weight:500;line-height:1.3">${ch}</div><div style="font-size:1.65rem;font-weight:800;color:${score?c2:'var(--tx3)'};line-height:1;margin-bottom:.28rem;letter-spacing:-.025em">${score}<span style="font-size:.82rem">%</span></div><div style="font-size:.63rem;color:var(--tx3);margin-bottom:.38rem;font-family:var(--m)">${done}/${all.length}</div>${bar(score,c2,3)}<div style="font-size:.6rem;color:${c2};margin-top:.38rem;text-align:right;opacity:.7">${ex?'▲':'▼'}</div></div>`;
  }).join('');
  rExp();
}
function switchSub(s){ASUB=s;EXP=null;rHeat();}
function togCh(k){EXP=EXP===k?null:k;rHeat();}
function rExp(){
  const p=$('#expanel');if(!EXP){p.innerHTML='';return;}
  const subs=S.subtopics||{},scores=S.topic_scores||{},chk=S.checked||{};
  const[sub,ch]=EXP.split('::');const c=SC[sub]||'#6366f1';
  const all=subs[EXP]||[],done=all.filter(s=>chk[`${EXP}::${s}`]).length;
  const score=scores[EXP]||0,allDone=all.length>0&&all.every(s=>chk[`${EXP}::${s}`]);
  const lbl=score<40?'Needs Work':score<70?'In Progress':score<100?'Almost There':'Mastered ✓';
  const rows=all.map(st=>{
    const sk=`${EXP}::${st}`,ck=!!chk[sk];
    return `<div class="subrow${ck?' on':''}" onclick="togSub('${sub}','${ch}','${st.replace(/'/g,"\\'")}')"><div class="chk${ck?' on':''}">${ck?'<span style="color:#fff;font-size:.62rem;font-weight:700">✓</span>':''}</div><span style="font-size:.78rem;font-weight:${ck?600:400};color:${ck?'var(--tx)':'var(--tx2)'}">${st}</span></div>`;
  }).join('');
  p.className='up';
  p.innerHTML=`<div class="flat mt-m" style="border:1.5px solid ${c}30;background:linear-gradient(135deg,${c}07,var(--sr))">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.9rem">
      <div>${chip(sub,c)}<div style="font-size:1.2rem;font-weight:800;margin-top:.38rem;letter-spacing:-.02em">${ch}</div><div style="font-size:.72rem;color:var(--tx3);margin-top:.18rem">${done} of ${all.length} done</div></div>
      <div style="text-align:right"><div style="font-size:2.2rem;font-weight:800;color:${c};line-height:1;letter-spacing:-.025em">${score}<span style="font-size:.9rem">%</span></div>${chip(lbl,scColor(score))}</div>
    </div>
    ${bar(score,c,6)}
    <div style="display:flex;align-items:center;justify-content:space-between;margin:1rem 0;padding:.7rem 0;border-top:1.5px solid var(--bd);border-bottom:1.5px solid var(--bd)">
      <button onclick="togAll('${sub}','${ch}')" style="display:flex;align-items:center;gap:.45rem;background:transparent;border:none;cursor:pointer;font-weight:700;font-size:.78rem;color:${c}">
        <div style="width:16px;height:16px;border-radius:4px;border:1.5px solid ${c};background:${allDone?c:'transparent'};display:flex;align-items:center;justify-content:center">${allDone?'<span style="color:#fff;font-size:.6rem;font-weight:700">✓</span>':''}</div>
        ${allDone?'Uncheck All':'Mark All Done'}
      </button>
      <span style="font-size:.67rem;color:var(--tx3);font-family:var(--m)">each = ${Math.round(100/Math.max(all.length,1))}%</span>
    </div>
    <div class="g-sub">${rows}</div>
    ${score===100?`<div style="margin-top:.9rem;padding:.8rem;background:rgba(16,185,129,.1);border:1.5px solid rgba(16,185,129,.28);border-radius:var(--r);text-align:center"><div style="font-weight:800;color:var(--grn)">Chapter Mastered 🏆</div><div style="font-size:.7rem;color:var(--tx3);margin-top:.15rem">This definitely comes in JEE.</div></div>`:''}
  </div>`;
}
async function togSub(sub,ch,st){
  const r=await api('/api/toggle_sub',{subject:sub,chapter:ch,subtopic:st});
  const ck=`${sub}::${ch}`,sk=`${ck}::${st}`;
  if(!S.checked)S.checked={};S.checked[sk]=r.checked;
  if(!S.topic_scores)S.topic_scores={};S.topic_scores[ck]=r.score;
  rHeat();rDash();
}
async function togAll(sub,ch){
  const r=await api('/api/toggle_all',{subject:sub,chapter:ch});
  const ck=`${sub}::${ch}`,all=(S.subtopics||{})[ck]||[];
  if(!S.checked)S.checked={};
  all.forEach(s=>{S.checked[`${ck}::${s}`]=r.score===100;});
  if(!S.topic_scores)S.topic_scores={};S.topic_scores[ck]=r.score;
  rHeat();rDash();
}

// ════════════════════════════════════════════════════════
// ANALYTICS
// ════════════════════════════════════════════════════════
function rAn(){
  const{mock_tests:tests,study_log:log,topic_scores:sc}=S;let html='';
  if(!tests||!tests.length){
    html+=`<div class="card mb-m"><div style="text-align:center;padding:2.5rem"><div style="font-size:1.8rem;margin-bottom:.65rem">📊</div><div style="font-weight:700;color:var(--tx2);margin-bottom:.35rem">No mock test data yet</div><div style="font-size:.8rem;color:var(--tx3)">Add tests in <span style="color:var(--phy)">Mock Tests</span> tab to see charts.</div></div></div>`;
  } else {
    const sn=getSubNames();
    const bars=tests.map(t=>{
      const sc2=t.scores||{};
      const trio=sn.map(s=>`<div class="bc" title="${s}: ${sc2[s]||0}%" style="height:${sc2[s]||0}%;background:linear-gradient(180deg,${SC[s]||'#666'},${SC[s]||'#666'}aa)"></div>`).join('');
      return `<div class="bg"><div class="bt2">${trio}</div><div style="font-size:.56rem;color:var(--tx3);font-family:var(--m);margin-top:3px">${(t.date||'').slice(5)}</div></div>`;
    }).join('');
    const gls=[25,50,75,100].map(v=>`<div class="gl" style="bottom:${v}%"><span style="font-size:.52rem;color:var(--tx3);font-family:var(--m)">${v}</span></div>`).join('');
    html+=`<div class="card mb-m"><div class="lbl mb-m">Score Trend</div><div class="cw">${gls}${bars}</div><div style="display:flex;gap:.9rem;margin-top:.7rem">${sn.map(s=>`<div style="display:flex;align-items:center;gap:.3rem"><div style="width:8px;height:8px;border-radius:2px;background:${SC[s]||'#666'}"></div><span style="font-size:.7rem;color:var(--tx3)">${s}</span></div>`).join('')}</div></div>`;
    if(tests.length>=2){
      const n=tests.length;
      const pts=tests.map((t,i)=>`${(i/(n-1)*100).toFixed(1)},${(100-t.percentile).toFixed(1)}`).join(' ');
      const poly=`0,100 ${pts} 100,100`;
      const dots=tests.map((t,i)=>{const x=(i/(n-1)*100).toFixed(1),y=(100-t.percentile).toFixed(1);return`<circle cx="${x}%" cy="${y}%" r="3.5" fill="#8b5cf6"/><circle cx="${x}%" cy="${y}%" r="7" fill="#8b5cf6" fill-opacity=".14"/><text x="${x}%" y="${(parseFloat(y)-5).toFixed(1)}%" text-anchor="middle" style="font-family:var(--m);font-size:7.5px;fill:#8b5cf6">${t.percentile}%</text>`;}).join('');
      html+=`<div class="card mb-m"><div class="lbl mb-m">Percentile Trajectory</div><div style="position:relative;height:130px;margin-top:.4rem"><div style="position:absolute;left:0;right:0;bottom:99%;border-top:1px dashed rgba(245,158,11,.4);display:flex;justify-content:flex-end"><span style="font-size:.58rem;color:#f59e0b;padding:0 .28rem;font-family:var(--m)">99%ile</span></div><svg width="100%" height="100%" style="overflow:visible"><defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#8b5cf6" stop-opacity=".18"/><stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/></linearGradient></defs><polygon points="${poly}" fill="url(#g1)"/><polyline points="${pts}" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-linejoin="round"/>${dots}</svg></div></div>`;
    }
  }
  // Calendar
  const days=[];for(let i=0;i<30;i++){const d=new Date();d.setDate(d.getDate()-(29-i));const k=d.toISOString().split('T')[0];days.push({key:k,date:d.getDate(),h:(log||{})[k]||0});}
  const cals=days.map(({key,date,h})=>{
    const a=h>0?0.12+Math.min(h/12,1)*.78:0,isEd=CAL_ED===key;
    const bg=h>0?`rgba(99,102,241,${a.toFixed(2)})`:'var(--sr2)';
    const inner=isEd?`<input type="number" id="ci-${key}" min="0" max="24" step=".5" value="${h}" onclick="event.stopPropagation()" onblur="saveCalD('${key}')" onkeydown="if(event.key==='Enter')saveCalD('${key}');if(event.key==='Escape'){CAL_ED=null;rAn()}" autofocus/>`:
      `<span style="font-size:.52rem;color:var(--tx3);font-family:var(--m)">${date}</span>${h>0?`<span style="font-size:.6rem;color:var(--phy);font-family:var(--m);font-weight:600">${h}h`:'<span style="font-size:.52rem;color:var(--tx3)">+</span>'}</span>`;
    return `<div class="cc" style="background:${bg};${h>0?'border-color:rgba(99,102,241,.3)':''}${isEd?';border-color:var(--phy)':''}" title="${key}: ${h}h — click to edit" onclick="CAL_ED='${key}';rAn()">${inner}</div>`;
  }).join('');
  const totH=days.reduce((a,{h})=>a+h,0);
  html+=`<div class="flat mb-m"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem"><div class="lbl">30-Day Activity</div><span style="font-size:.7rem;color:var(--tx3)">Click any day to edit</span></div><div class="g-cal">${cals}</div><div style="font-size:.72rem;color:var(--tx3);margin-top:.7rem">Total: <span style="font-family:var(--m);color:var(--phy);font-weight:600">${totH.toFixed(1)}h</span> · Avg: <span style="font-family:var(--m);color:var(--phy);font-weight:600">${(totH/30).toFixed(1)}h/day</span></div></div>`;
  // Mastery bars
  html+=`<div class="flat"><div class="lbl" style="margin-bottom:.3rem">Subject Mastery</div><div style="font-size:.72rem;color:var(--tx3);margin-bottom:.9rem">Based on your heatmap progress</div>${Object.keys(SC).map(sub=>{const vals=Object.entries(sc||{}).filter(([k])=>k.startsWith(sub)).map(([,v])=>v);const avg=vals.length?(vals.reduce((a,b)=>a+b,0)/vals.length).toFixed(1):'0';const c=SC[sub];return`<div style="display:flex;align-items:center;gap:.9rem;margin-bottom:.8rem"><div style="width:88px;font-weight:700;font-size:.82rem;color:${c}">${sub}</div><div style="flex:1">${bar(parseFloat(avg),c,7)}</div><div style="font-size:.78rem;color:var(--tx3);font-family:var(--m);width:40px;text-align:right">${avg}%</div></div>`;}).join('')}</div>`;
  $('#anc').innerHTML=html;
  if(CAL_ED){const inp=document.getElementById(`ci-${CAL_ED}`);if(inp){inp.focus();inp.select();}}
}
async function saveCalD(key){
  const inp=document.getElementById(`ci-${key}`);const h=inp?parseFloat(inp.value):0;
  CAL_ED=null;await api('/api/set_hours',{date:key,hours:isNaN(h)?0:h});
  if(!S.study_log)S.study_log={};if(h>0)S.study_log[key]=h;else delete S.study_log[key];
  rAn();updateHdr();
}

// ════════════════════════════════════════════════════════
// TIMER
// ════════════════════════════════════════════════════════
function setMode(m,s){
  T_MODE=m;T_MSEC=s;
  document.querySelectorAll('#tmodes .st').forEach((b,i)=>b.classList.toggle('on',['p','d','b'][i]===m));
}
function toggleTimer(){
  if(T_RUN){clearInterval(T_INT);T_RUN=false;$('#tstrt').innerHTML='▶ Start';$('#tstat').textContent='PAUSED';$('#tring').style.opacity='.25';}
  else{T_RUN=true;$('#tstrt').innerHTML='⏸ Pause';$('#tstat').textContent='GRINDING ⚡';$('#tring').style.opacity='1';T_INT=setInterval(()=>{T_SEC++;updateTD();},1000);}
}
function updateTD(){
  $('#tdisp').textContent=fmtT(T_SEC);
  const circ=628.3,pct=(T_SEC%T_MSEC)/T_MSEC;
  $('#tring').setAttribute('stroke-dashoffset',String(circ*(1-pct)));
}
async function stopTimer(){
  clearInterval(T_INT);T_RUN=false;$('#tstrt').innerHTML='▶ Start';$('#tstat').textContent='READY';
  $('#tring').style.opacity='.25';$('#tring').setAttribute('stroke-dashoffset','628.3');
  if(T_SEC>60){
    const h=T_SEC/3600;SESS.push({dur:T_SEC,time:new Date().toLocaleTimeString()});TSEC_TOT+=T_SEC;
    await api('/api/log_hours',{date:today(),hours:h});
    if(!S.study_log)S.study_log={};S.study_log[today()]=(S.study_log[today()]||0)+h;
    updateHdr();rSess();toast(`Session logged: ${fmtT(T_SEC)}`);
  }
  T_SEC=0;$('#tdisp').textContent='00:00:00';
}
function rSess(){
  if(!SESS.length){$('#sescard').style.display='none';return;}
  $('#sescard').style.display='block';
  $('#seslist').innerHTML=SESS.map((s,i)=>`<div style="display:flex;justify-content:space-between;align-items:center;padding:.48rem 0;border-bottom:1.5px solid var(--bd)"><span style="font-size:.78rem;color:var(--tx3)">Session ${i+1}</span><span style="font-family:var(--m);font-size:.78rem;color:var(--phy);font-weight:600">${fmtT(s.dur)}</span><span style="font-size:.66rem;color:var(--tx3);font-family:var(--m)">${s.time}</span></div>`).join('');
  $('#sestot').textContent=fmtT(TSEC_TOT);
}

// ════════════════════════════════════════════════════════
// MOCK TESTS
// ════════════════════════════════════════════════════════
function getSubNames(){return Object.keys(SC);}
function getMockScores(){
  const scores={};
  document.querySelectorAll('#mock-inputs input[data-sub]').forEach(el=>{const v=parseFloat(el.value);if(!isNaN(v))scores[el.dataset.sub]=v;});
  return scores;
}
function prevTest(){
  const scores=getMockScores(), sn=getSubNames(), box=$('#prevbox');
  if(Object.keys(scores).length===sn.length){
    const pct=cpct(...Object.values(scores));const[col,lbl]=pinfo(pct);
    $('#ppct').textContent=pct.toFixed(1);
    const b=$('#pbadge');b.textContent=lbl;b.style.cssText=`color:${col};background:${col}15;border-color:${col}40`;
    box.style.display='flex';
  } else box.style.display='none';
}
async function addTest(){
  const scores=getMockScores(),sn=getSubNames(),date=$('#idate').value||today();
  if(Object.keys(scores).length<sn.length){toast('Enter all scores','err');return;}
  const r=await api('/api/add_test',{scores,date});
  document.querySelectorAll('#mock-inputs input[data-sub]').forEach(el=>el.value='');$('#prevbox').style.display='none';
  S.mock_tests=(S.mock_tests||[]).concat([{date,scores,percentile:r.percentile,id:r.id}]);
  S.predicted_pct=r.percentile;updateHdr();rMock();toast(`Added: ${r.percentile.toFixed(1)}%ile`);
}
async function delTest(id){
  await api('/api/del_test',{id});S.mock_tests=(S.mock_tests||[]).filter(t=>t.id!==id);rMock();toast('Test deleted');
}
async function saveEdit(id){
  const scores={},sn=getSubNames(),date=$(`#ed${id}`).value;
  sn.forEach(s=>{const el=$(`#es_${id}_${s.replace(/\\s+/g,'_')}`);if(el)scores[s]=parseFloat(el.value);});
  if(Object.keys(scores).length<sn.length)return;
  const r=await api('/api/edit_test',{id,scores,date});
  const t=(S.mock_tests||[]).find(t=>t.id===id);
  if(t){t.scores=scores;t.percentile=r.percentile;if(date)t.date=date;}
  EDT_ID=null;rMock();toast('Test updated');
}
async function clrTests(){
  if(!CLR_CNF){CLR_CNF=true;rMock();return;}
  await api('/api/clear_tests',{});S.mock_tests=[];CLR_CNF=false;EDT_ID=null;rMock();toast('All tests cleared');
}
function rMock(){
  const tests=S.mock_tests||[],sn=getSubNames();
  $('#tcnt').textContent=`(${tests.length} tests)`;
  $('#clrrow').innerHTML=tests.length===0?'':CLR_CNF?`<div class="flex gap-s ctr"><span style="font-size:.76rem;color:var(--red)">Delete all?</span><button class="btn bd2 bxs" onclick="clrTests()">Yes, clear</button><button class="btn bo bxs" onclick="CLR_CNF=false;rMock()">Cancel</button></div>`:`<button class="btn bd2 bsm" onclick="clrTests()">🗑 Clear All</button>`;
  if(!tests.length){$('#thist').innerHTML=`<div style="text-align:center;padding:2.5rem"><div style="font-size:1.75rem;margin-bottom:.6rem">📋</div><div style="font-size:.86rem;color:var(--tx3)">No tests logged yet. Add your first above.</div></div>`;return;}
  const rows=[...tests].reverse().map(t=>{
    const sc2=t.scores||{};const vals=Object.values(sc2);
    const avg=vals.length?(vals.reduce((a,b)=>a+b,0)/vals.length).toFixed(1):'—';
    const gap=(99-(t.percentile||0)).toFixed(1);
    const pc=(t.percentile||0)>=95?'#10b981':(t.percentile||0)>=85?'#f59e0b':'#ef4444';
    const gc=gap<5?'#10b981':gap<15?'#f59e0b':'#ef4444';
    const isEd=EDT_ID===t.id;
    if(isEd)return`<tr style="background:rgba(99,102,241,.06)"><td><input type="date" id="ed${t.id}" value="${t.date}" style="background:var(--bg1);border:1.5px solid var(--bd);border-radius:6px;color:var(--tx);padding:.28rem .48rem;font-size:.74rem"/></td>${sn.map(s=>`<td><input id="es_${t.id}_${s.replace(/\\s+/g,'_')}" type="number" value="${sc2[s]||0}" min="0" max="100" style="width:55px;background:var(--bg1);border:1.5px solid ${SC[s]||'var(--bd)'};border-radius:6px;color:${SC[s]||'var(--tx)'};padding:.28rem .48rem;font-size:.74rem;font-family:var(--m)"/></td>`).join('')}<td>—</td><td>—</td><td>—</td><td><div class="flex gap-xs"><button class="btn bs bxs" onclick="saveEdit(${t.id})">Save</button><button class="btn bo bxs" onclick="EDT_ID=null;rMock()">✕</button></div></td></tr>`;
    return`<tr><td style="font-family:var(--m);font-size:.73rem;color:var(--tx3)">${t.date}</td>${sn.map(s=>`<td style="color:${SC[s]||'var(--tx)'};font-family:var(--m);font-weight:600">${sc2[s]||0}%</td>`).join('')}<td style="font-family:var(--m)">${avg}%</td><td>${chip(`${(t.percentile||0).toFixed?t.percentile.toFixed(1):t.percentile}%ile`,pc)}</td><td style="font-family:var(--m);font-size:.72rem;color:${gc}">-${gap}</td><td><div class="flex gap-xs"><button class="btn bo bxs" onclick="EDT_ID=${t.id};rMock()">Edit</button><button class="btn bd2 bxs" onclick="delTest(${t.id})">✕</button></div></td></tr>`;
  }).join('');
  $('#thist').innerHTML=`<div class="tbl-w"><table class="tbl"><thead><tr>${['Date',...sn,'Avg','Percentile','Gap to 99','Actions'].map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div>`;
}

// ════════════════════════════════════════════════════════
// DOUBTS
// ════════════════════════════════════════════════════════
$('#dtype').addEventListener('change',function(){$('#dimgsec').style.display=this.value==='image'?'block':'none';});
async function loadDoubts(f){
  DF=f;
  document.querySelectorAll('#t-doubts .st').forEach(b=>b.classList.toggle('on',b.textContent.trim().includes(f==='All'?'All':f)));
  const rows=await fetch(`/api/doubts${f&&f!=='All'?'?subject='+f:''}`).then(r=>r.json()).catch(()=>[]);
  $('#dlist').innerHTML=rows.length?rows.map(d=>{
    const sc2=SC[d.subject]||'#52567a';
    return`<div class="dcard${d.solved?' solved':''}" onclick="openDoubt(${d.id})">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.55rem">
        <div style="display:flex;align-items:center;gap:.55rem">
          <div style="width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,var(--phy),var(--mat));display:flex;align-items:center;justify-content:center;font-size:.85rem">${d.avatar||'🎯'}</div>
          <div><div style="font-weight:600;font-size:.83rem">${d.name||d.username}</div><div style="font-size:.68rem;color:var(--tx3)">@${d.username} · ${rel(d.created_at)}</div></div>
        </div>
        <div class="flex gap-s">${chip(d.subject,sc2)}${d.solved?chip('✓ Solved','#10b981'):''}</div>
      </div>
      <div style="font-weight:700;font-size:.92rem;margin-bottom:.38rem">${d.title}</div>
      <div style="font-size:.78rem;color:var(--tx2);line-height:1.5;margin-bottom:.55rem">${d.body.slice(0,130)}${d.body.length>130?'…':''}</div>
      <div style="font-size:.7rem;color:var(--tx3)">💬 ${d.replies||0} replies</div>
    </div>`;
  }).join(''):`<div style="text-align:center;padding:2.5rem;color:var(--tx3);font-size:.86rem">No doubts yet. Be the first to post!</div>`;
}
async function openDoubt(id){
  const{doubt:d,replies}=await fetch(`/api/doubt/${id}`).then(r=>r.json());
  $('#ddtit').textContent=d.title;
  const isOwner=ME&&ME.id===d.user_id;
  const sc2=SC[d.subject]||'#52567a';
  const reps=replies.map(r=>{
    const isMe=ME&&ME.id===r.user_id;
    return`<div class="drep"><div style="display:flex;justify-content:space-between;margin-bottom:.38rem"><div style="font-weight:600;font-size:.8rem">${r.name||r.username} <span style="color:var(--tx3);font-weight:400;font-size:.72rem">· ${rel(r.created_at)}</span></div>${isMe?`<button class="btn bd2 bxs" onclick="delReply(${r.id},${id})">✕</button>`:''}</div><div style="font-size:.8rem;color:var(--tx2);line-height:1.55">${r.body}</div></div>`;
  }).join('');
  $('#ddcon').innerHTML=`
    <div style="display:flex;justify-content:space-between;margin-bottom:.9rem">
      <div class="flex gap-s">${chip(d.subject,sc2)}${d.solved?chip('✓ Solved','#10b981'):''}</div>
      ${isOwner?`<div class="flex gap-s"><button class="btn bo bxs" onclick="markSolved(${d.id})">${d.solved?'Mark Unsolved':'Mark Solved'}</button><button class="btn bd2 bxs" onclick="delDoubt(${d.id})">Delete</button></div>`:''}
    </div>
    <div style="font-size:.85rem;color:var(--tx2);line-height:1.6;padding:.85rem;background:var(--bg1);border-radius:var(--r);margin-bottom:1rem">${d.body}</div>
    ${d.media_b64&&d.media_type==='image'?`<img src="${d.media_b64}" style="max-width:100%;border-radius:var(--r);margin-bottom:.9rem"/>`:''}
    <div class="lbl mb-s">${replies.length} Replies</div>
    ${reps}
    <div style="margin-top:.9rem">
      <textarea class="inp" id="rb-${id}" placeholder="Write your reply..." rows="3"></textarea>
      <button class="btn bf mt-s" onclick="postReply(${id})">Post Reply</button>
    </div>`;
  openMod('ddm');
}
async function postReply(did){
  const b=$(`#rb-${did}`).value.trim();if(!b)return;
  await api('/api/post_reply',{doubt_id:did,body:b});
  openDoubt(did);toast('Reply posted');
}
async function delReply(rid,did){await api('/api/del_reply',{id:rid});openDoubt(did);}
async function markSolved(did){await api('/api/solve_doubt',{id:did});openDoubt(did);loadDoubts(DF);}
async function delDoubt(did){await api('/api/del_doubt',{id:did});closeMod('ddm');loadDoubts(DF);toast('Doubt deleted');}
async function postDoubt(){
  const title=$('#dtit').value.trim(),body2=$('#dbod').value.trim();
  if(!title||!body2){toast('Title and body required','err');return;}
  let mb64='';
  if($('#dtype').value==='image'){
    const f=$('#dimg').files[0];
    if(f)mb64=await new Promise(res=>{const r=new FileReader();r.onload=()=>res(r.result);r.readAsDataURL(f);});
  }
  const r=await api('/api/post_doubt',{title,body:body2,subject:$('#dsub').value,media_type:$('#dtype').value,media_b64:mb64});
  closeMod('pdm');$('#dtit').value='';$('#dbod').value='';
  loadDoubts(DF);toast('Doubt posted!');
}

// ════════════════════════════════════════════════════════
// FRIENDS & LEADERBOARD
// ════════════════════════════════════════════════════════
async function rFriends(){
  const{friends,pending}=S;
  if(pending&&pending.length){
    $('#preqs').classList.remove('hide');
    $('#preqlist').innerHTML=pending.map(p=>`<div class="lbr"><div class="lba">${p.avatar||'🎯'}</div><div style="flex:1"><div style="font-weight:600;font-size:.86rem">${p.name||p.username}</div><div style="font-size:.7rem;color:var(--tx3)">@${p.username} · ${rel(p.created_at)}</div></div><div class="flex gap-s"><button class="btn bs bsm" onclick="accFriend('${p.username}')">Accept</button></div></div>`).join('');
  } else $('#preqs').classList.add('hide');
  const entries=[{username:ME.username,name:ME.name,avatar:ME.avatar,predicted_pct:S.predicted_pct,total_hours:S.total_hours,mastered:Object.values(S.topic_scores||{}).filter(v=>v===100).length,streak:S.streak,isMe:true}];
  for(const f of(friends||[])){
    if(!LB_CACHE[f.id])LB_CACHE[f.id]=await fetch(`/api/friend_stats/${f.id}`).then(r=>r.json()).catch(()=>({}));
    entries.push({...LB_CACHE[f.id],friend_id:f.id});
  }
  entries.sort((a,b)=>(b.predicted_pct||0)-(a.predicted_pct||0));
  const medals=['🥇','🥈','🥉'];
  $('#lboard').innerHTML=entries.length<2?`<div style="text-align:center;padding:2.5rem;color:var(--tx3);font-size:.86rem">Add friends to compete on the leaderboard!</div>`:
    entries.map((e,i)=>{
      return`<div class="lbr${e.isMe?' me':''}">
        <span style="color:var(--tx3);font-size:.88rem;font-family:var(--m);width:24px;text-align:center;flex-shrink:0">${medals[i]||i+1}</span>
        <div class="lba">${e.avatar||'🎯'}</div>
        <div style="flex:1"><div style="font-weight:700;font-size:.88rem">${e.name||e.username} ${e.isMe?'<span style="font-size:.68rem;color:var(--phy)">(you)</span>':''}</div><div style="font-size:.7rem;color:var(--tx3)">@${e.username}</div></div>
        <div style="display:grid;grid-template-columns:repeat(4,auto);gap:1.1rem;text-align:center">
          ${[[e.predicted_pct?e.predicted_pct.toFixed(1)+'%':'—','%ile','#8b5cf6'],[(e.total_hours||0).toFixed(0)+'h','Hours','#6366f1'],[e.mastered||0,'Mastered','#10b981'],[(e.streak||0)+'d','Streak','#f97316']].map(([v,l,c])=>`<div><div style="font-size:.62rem;color:var(--tx3)">${l}</div><div style="font-weight:700;font-size:.86rem;color:${c};font-family:var(--m)">${v}</div></div>`).join('')}
        </div>
        ${!e.isMe?`<button class="btn bd2 bxs" onclick="remFriend(${e.friend_id})">Remove</button>`:''}
      </div>`;
    }).join('');
}
async function addFriend(){
  const un=$('#fui').value.trim().replace('@','');const errEl=$('#ferr');errEl.style.display='none';
  const r=await api('/api/add_friend',{username:un});
  if(r.error){errEl.textContent=r.error;errEl.style.display='block';return;}
  closeMod('afm');$('#fui').value='';toast('Friend request sent!');
}
async function accFriend(un){
  await api('/api/accept_friend',{username:un});
  S.pending=(S.pending||[]).filter(p=>p.username!==un);
  LB_CACHE={};
  const fbdg=$('#fbdg');
  if((S.pending||[]).length>0){fbdg.textContent=S.pending.length;fbdg.classList.remove('hide');}else fbdg.classList.add('hide');
  rFriends();toast('Friend accepted!');
}
async function remFriend(fid){
  if(!confirm('Remove this friend?'))return;
  await api('/api/remove_friend',{friend_id:fid});
  S.friends=(S.friends||[]).filter(f=>f.id!==fid);delete LB_CACHE[fid];rFriends();toast('Friend removed');
}

// ════════════════════════════════════════════════════════
// ACTIVITY
// ════════════════════════════════════════════════════════
function rActivity(){
  const acts=S.activity||[];
  $('#actlist').innerHTML=acts.length?acts.map(a=>`<div class="act"><div class="adot"></div><div style="flex:1"><div style="font-weight:600;font-size:.84rem">${a.action}</div>${a.detail?`<div style="font-size:.74rem;color:var(--tx3);margin-top:.12rem">${a.detail}</div>`:''}<div style="font-size:.66rem;color:var(--tx3);margin-top:.18rem;font-family:var(--m)">${rel(a.created_at)}</div></div></div>`).join(''):`<div style="text-align:center;padding:2rem;color:var(--tx3);font-size:.84rem">No activity yet.</div>`;
}

// ════════════════════════════════════════════════════════
// PROFILE & SETTINGS
// ════════════════════════════════════════════════════════
function toggleDD(){$('#pdd').classList.toggle('on');}
function toggleWN(){$('#wn').classList.toggle('on');}
async function switchExam(newExam){
  const old=S.exam_type||'JEE';
  if(newExam===old)return;
  const ed=EXAM_DATA[newExam]||{};
  const ok=await siteConfirm({
    icon:ed.icon||'📝',iconType:'warn',
    title:'Switch to '+newExam+'?',
    msg:'The page will refresh to load your new subjects and topics. Your existing progress will be preserved.',
    confirmText:'Switch Exam',cancelText:'Stay on '+old,confirmClass:'bf'
  });
  if(!ok){$('#pexam').value=old;return;}
  try{await api('/api/profile/update',{exam_type:newExam});}catch(e){}
  window.location.href=window.location.pathname+'?t='+Date.now();
}
function openProfile(){
  if(!ME)return;
  $('#pn').value=ME.name||'';$('#pb').value=ME.bio||'';$('#pc').value=ME.college||'';$('#pe').value=ME.exam_date||'';
  const sel=$('#pexam');sel.innerHTML='';
  const elist=S.exam_list||Object.keys(EXAM_DATA).map(k=>({key:k,...EXAM_DATA[k]}));
  elist.forEach(ex=>{
    const k=ex.key||ex;
    const o=document.createElement('option');o.value=k;o.textContent=(ex.icon||'')+ ' '+(ex.name||k);
    if(k===(S.exam_type||'JEE'))o.selected=true;
    sel.appendChild(o);
  });
  SEL_EMO=ME.avatar||'🎯';buildEmoGrid('peg','selPEmo');openMod('pm2');
}
function openSettings(){openMod('sm');}
async function saveProf(){
  const dn=$('#pn').value,bio=$('#pb').value,college=$('#pc').value,exam=$('#pe').value;
  const newExam=$('#pexam').value;
  const oldExam=S.exam_type||'JEE';
  const payload={name:dn,bio,college,exam_date:exam,avatar:SEL_EMO,exam_type:newExam};
  const op=$('#op').value,np=$('#np').value,np2=$('#np2').value;
  if(op&&np){
    if(np!==np2){toast('Passwords do not match','err');return;}
    payload.old_password=op;payload.new_password=np;
  }
  const r=await api('/api/profile/update',payload);
  if(r.error){toast(r.error,'err');return;}
  if(ME){ME.name=dn;ME.bio=bio;ME.college=college;ME.exam_date=exam;ME.avatar=SEL_EMO;}
  $('#dd-name').textContent=dn||ME?.username;$('#avbtn').textContent=SEL_EMO;
  ['#op','#np','#np2'].forEach(id=>$(id).value='');
  closeMod('pm2');
  if(newExam!==oldExam){toast('Switching to '+newExam+'...');await boot();toast('Exam changed to '+newExam);}
  else{toast('Profile updated');}
}
async function deleteAccount(){
  const ok=await siteConfirm({
    icon:'🗑️',iconType:'danger',
    title:'Delete your account?',
    msg:'This action is PERMANENT. All your data, progress, mock tests, and study logs will be erased forever.',
    confirmText:'Delete Forever',cancelText:'Keep Account',confirmClass:'bd2'
  });
  if(!ok)return;
  const pw=await siteConfirm({
    icon:'🔒',iconType:'danger',
    title:'Confirm with password',
    msg:'Enter your password to permanently delete your account.',
    confirmText:'Delete My Account',cancelText:'Cancel',confirmClass:'bd2',
    inputPlaceholder:'Your password',inputType:'password'
  });
  if(!pw)return;
  const r=await api('/api/delete_account',{password:pw});
  if(r.error){toast(r.error,'err');return;}
  toast('Account deleted. Goodbye!');
  setTimeout(()=>location.reload(),1500);
}
function toggleTheme(){
  const cur=document.documentElement.getAttribute('data-theme');
  const next=cur==='dark'?'light':'dark';
  document.documentElement.setAttribute('data-theme',next);
  updateThemeUI();api('/api/profile/update',{theme:next});if(ME)ME.theme=next;
}
function updateThemeUI(){
  const isDark=(ME?.theme||'dark')==='dark';
  $('#thbtn').textContent=isDark?'🌙':'☀️';
  const tgl=$('#thtgl');if(tgl)tgl.classList.toggle('on',isDark);
}
async function dlReport(){
  toast('Generating PDF report...');
  const a=document.createElement('a');a.href='/api/report';a.download='StudyOS_Report.pdf';a.click();
}

// ════════════════════════════════════════════════════════
// BOOT
// ════════════════════════════════════════════════════════
buildEmoGrid('aeg','selEmo');
buildExamGrid();
$('#idate').value=today();
boot().catch(()=>{});
</script>
</body>
</html>"""

# ═══════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════
def main():
    init_db()
    srv = HTTPServer(("localhost", PORT), H)
    url = f"http://localhost:{PORT}"
    print(f"\n  ⚡ StudyOS  →  {url}\n  Database: jeeos.db\n  Press Ctrl+C to stop\n")
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋 Stopped. See you tomorrow.")
        srv.shutdown()

if __name__ == "__main__":
    main()
