# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
DATABASE_NAME = "mwalimu.db"

CBC = {
    "Grade 1": {
        "Mathematical Activities": {
            "Numbers": {
                "Counting & Recognition": [
                    "Count numbers 1 to 50 sequentially",
                    "Represent quantities using concrete classroom objects",
                    "Identify symbols for numbers 1 to 20"
                ]
            },
            "Geometry": {
                "Shapes": [
                    "Identify circles, triangles, and rectangles in the environment",
                    "Make patterns using basic geometric shapes"
                ]
            }
        },
        "Language Activities": {
            "Listening & Speaking": {
                "Greetings & Self-Awareness": [
                    "Respond politely to greetings from peers and teachers",
                    "Pronounce basic vocabulary sounds clearly",
                    "State their name and express basic needs cleanly"
                ]
            },
            "Reading": {
                "Letter Sounds": [
                    "Recognize and read simple alphabet vowel sounds",
                    "Blend two-letter consonant-vowel combinations"
                ]
            }
        },
        "Environmental Activities": {
            "Our School": {
                "Cleanliness": [
                    "Identify clean classroom and school environment habits",
                    "Demonstrate proper handwashing techniques at school"
                ]
            }
        },
        "Religious Education (CRE/IRE)": {
            "Creation": {
                "My Self": [
                    "Appreciate unique physical features as a creation of God",
                    "State names of family members and show love for them"
                ]
            }
        },
        "Creative Activities": {
            "Drawing & Painting": {
                "Basic Patterns": [
                    "Draw basic geometric lines and color within boundaries",
                    "Create simple block prints using fingers or leaves"
                ]
            }
        }
    },
    "Grade 2": {
        "Mathematical Activities": {
            "Numbers": {
                "Addition & Subtraction": [
                    "Add two-digit numbers without regrouping",
                    "Solve basic real-life word problems involving subtraction",
                    "Count forward and backward by 2s up to 100"
                ]
            },
            "Measurement": {
                "Time": [
                    "Tell time by full hours using an analogue clock face",
                    "Name the days of the week in chronological order"
                ]
            }
        },
        "Language Activities": {
            "Reading": {
                "Fluency": [
                    "Read short sentences aloud with correct pronunciation",
                    "Identify main characters in a simple illustrated storybook"
                ]
            },
            "Writing": {
                "Handwriting": [
                    "Form legible lowercase and uppercase letters neatly",
                    "Write simple three-letter words from dictation"
                ]
            }
        },
        "Environmental Activities": {
            "Our Home": {
                "Safety & Health": [
                    "Identify sharp objects to avoid in the household",
                    "Differentiate between clean and safe drinking water sources"
                ]
            }
        }
    },
    "Grade 3": {
        "Mathematical Activities": {
            "Numbers": {
                "Place Value": [
                    "Identify place value of digits up to hundreds",
                    "Read and write number names smoothly up to 1000",
                    "Multiply single digits using repeated addition concepts"
                ]
            },
            "Measurement": {
                "Money": [
                    "Identify Kenyan currency coins and notes up to 1000 shillings",
                    "Perform simple shopkeeper currency exchange configurations"
                ]
            }
        },
        "Language Activities": {
            "Writing": {
                "Spelling & Sentences": [
                    "Spell common environmental and household words correctly",
                    "Construct simple present tense sentences using word clues"
                ]
            }
        },
        "Environmental Activities": {
            "Weather & Sky": {
                "Elements of Weather": [
                    "Record daily changes in weather conditions on a chart",
                    "Identify uses of light and heat from the sun safely"
                ]
            }
        }
    },
    "Grade 4": {
        "Mathematics": {
            "Numbers": {
                "Fractions": [
                    "Identify fractions visually using shaded diagrams", 
                    "Compare fractions with same denominators", 
                    "Add fractions with same denominators"
                ],
                "Decimals": [
                    "Identify decimals using place value charts", 
                    "Compare decimals up to one decimal place"
                ]
            },
            "Measurement": {
                "Length": [
                    "Measure length using standard units (metres)", 
                    "Convert metres to centimetres accurately"
                ]
            }
        },
        "English": {
            "Reading": {
                "Comprehension": [
                    "Read short stories fluently and accurately", 
                    "Answer direct explicit questions from a passage"
                ]
            }
        },
        "Kiswahili": {
            "Kusikiliza na Kuzungumza": {
                "Adabu": [
                    "Kujifunza kutoa maamkizi ya heshima na adabu", 
                    "Kutumia maneno ya adabu kama tafadhali na asante"
                ]
            }
        },
        "Science and Technology": {
            "Living Things": {
                "Plants": [
                    "Classify local plants into flowering and non-flowering categories"
                ]
            }
        },
        "Social Studies": {
            "Our County": {
                "Physical Features": [
                    "Identify major hills, plains, and rivers in the county"
                ]
            }
        },
        "CRE": {
            "Christian Values": {
                "Respect": [
                    "Demonstrate respect for elders, teachers, and peers in daily life"
                ]
            }
        }
    },
    "Grade 5": {
        "Mathematics": {
            "Numbers": {
                "Multiplication & Division": [
                    "Multiply a 3-digit number by a 2-digit number",
                    "Divide numbers up to 3-digits by a 1-digit number without remainders"
                ]
            },
            "Geometry": {
                "Perimeter & Area": [
                    "Calculate the perimeter of rectangles and squares",
                    "Estimate area using grid square counting cards"
                ]
            }
        },
        "English": {
            "Language Structures": {
                "Punctuation & Nouns": [
                    "Use capital letters, commas, and full stops accurately",
                    "Form regular plural nouns by adding suffixes correctly"
                ]
            }
        },
        "Science and Technology": {
            "Environment": {
                "Waste Management": [
                    "Classify classroom waste into organic and inorganic types",
                    "Describe simple ways to reuse plastic containers effectively"
                ]
            },
            "Animals": {
                "Vertebrates": [
                    "List the five classes of vertebrate animals",
                    "Describe breathing habits of mammals versus amphibians"
                ]
            }
        },
        "Social Studies": {
            "Resources": {
                "Agriculture": [
                    "Identify major cash crops grown across regional zones",
                    "Describe methods used to conserve farm soils from erosion"
                ]
            }
        }
    },
    "Grade 6": {
        "Mathematics": {
            "Algebra": {
                "Algebraic Expressions": [
                    "Form simple algebraic expressions from word clues",
                    "Simplify expressions by collecting like terms smoothly"
                ]
            },
            "Data Handling": {
                "Graphs": [
                    "Read and interpret simple statistical bar graphs",
                    "Construct simple tallies to track inventory counts"
                ]
            }
        },
        "English": {
            "Writing": {
                "Composition Structure": [
                    "Write a coherent three-paragraph creative essay narrative",
                    "Apply descriptive adverbs to heighten storytelling plots"
                ]
            }
        },
        "Science and Technology": {
            "The Human Body": {
                "Excretory System": [
                    "Identify functions of major human skin structure layers",
                    "Describe methods of maintaining healthy kidneys and skin"
                ]
            }
        }
    },
    "Grade 7": {
        "Mathematics": {
            "Algebraic Expressions": {
                "Linear Equations": [
                    "Form linear equations from real-life situations", 
                    "Solve simple linear equations in one variable"
                ]
            },
            "Data Handling": {
                "Probability": [
                    "Identify possible outcomes of a simple event", 
                    "Calculate experimental probability from given sample charts"
                ]
            }
        },
        "English": {
            "Grammar": {
                "Nouns": [
                    "Identify singular and plural countable nouns"
                ]
            }
        },
        "Kiswahili": {
            "Sarufi": {
                "Aina za Maneno": [
                    "Kutambua nomino na vitenzi katika sentensi"
                ]
            }
        },
        "Science and Technology": {
            "Living Things": {
                "Plants": [
                    "Classify plants based on their structural characteristics", 
                    "Describe parts of a flowering plant and their specific functions"
                ]
            }
        },
        "Social Studies": {
            "Our Environment": {
                "Maps": [
                    "Interpret basic compass direction signs on local layout charts"
                ]
            }
        }
    },
    "Grade 8": {
        "Mathematics": {
            "Geometry": {
                "Angles & Shapes": [
                    "Calculate missing interior angles in triangles and quadrilaterals",
                    "Construct parallel lines using a straight edge and compass tool"
                ]
            }
        },
        "English": {
            "Literature": {
                "Short Stories": [
                    "Identify main thematic elements inside local folk narratives",
                    "Analyze character motives inside a short prose text extract"
                ]
            }
        },
        "Integrated Science": {
            "Matter": {
                "Elements & Compounds": [
                    "Distinguish between simple chemical mixtures and pure chemical compounds",
                    "State structural properties of metals versus non-metals"
                ]
            }
        }
    },
    "Form 1": {
        "English": {
            "Grammar": {
                "Parts of Speech": [
                    "Master usage of pronouns and introductory conjunctions"
                ]
            }
        },
        "Mathematics": {
            "Numbers & Algebra": {
                "Factors & Multiples": [
                    "Find the GCD and LCM of given integers", 
                    "Apply LCM to interval tracking problems"
                ]
            }
        },
        "Kiswahili": {
            "Fasihi Simulizi": {
                "Misingi ya Fasihi": [
                    "Kuelewa tanzu tofauti za fasihi ya mazungumzo"
                ]
            }
        },
        "Geography": {
            "Introduction": {
                "The Earth and Solar System": [
                    "Describe components of the solar system", 
                    "Calculate distances using map scales"
                ]
            }
        },
        "Physics": {
            "Measurement": {
                "Physical Quantities": [
                    "Measure length, mass, and time using standard lab equipment"
                ]
            }
        },
        "Chemistry": {
            "Introduction": {
                "Laboratory Safety & Apparatus": [
                    "Identify common laboratory apparatus and hazard symbols"
                ]
            }
        },
        "Biology": {
            "Introduction to Biology": {
                "Characteristics": [
                    "List the seven characteristics of living things"
                ]
            }
        },
        "Business Studies": {
            "Introduction": {
                "Business & Society": [
                    "Explain the role of business studies in day-to-day life"
                ]
            }
        },
        "History and Government": {
            "Introduction": {
                "Sources of History": [
                    "Differentiate between oral, written, and archaeological sources"
                ]
            }
        },
        "CRE": {
            "Introduction": {
                "The Bible": [
                    "Describe the composition, translation, and major divisions of the Bible"
                ]
            }
        }
    },
    "Form 2": {
        "English": {
            "Functional Writing": {
                "Letters & Memos": [
                    "Draft formal letters and official business memos"
                ]
            }
        },
        "Mathematics": {
            "Equations & Formulae": {
                "Quadratic Expressions": [
                    "Expand and factorize binomial equations completely"
                ]
            }
        },
        "Kiswahili": {
            "Ufahamu": {
                "Kusoma kwa Kina": [
                    "Kujibu maswali ya kifungu cha habari kwa usahihi"
                ]
            }
        },
        "Geography": {
            "Internal Land-forming Processes": {
                "Faulting": [
                    "Explain features resulting from faulting processes"
                ]
            }
        },
        "Physics": {
            "Mechanics": {
                "Turning Effect of a Force": [
                    "Apply the principle of moments to balance configurations"
                ]
            }
        },
        "Chemistry": {
            "Structure and Bonding": {
                "The Periodic Table": [
                    "Describe properties of elements across periods and down groups"
                ]
            }
        },
        "Biology": {
            "Transport": {
                "Transport in Plants": [
                    "Explain absorption of water and mineral salts through root hairs"
                ]
            }
        },
        "Business Studies": {
            "Forms of Business Units": {
                "Sole Proprietorships": [
                    "Analyze characteristics, advantages, and disadvantages of sole traders"
                ]
            }
        },
        "History and Government": {
            "Early History": {
                "Migration & Settlement": [
                    "Trace migration patterns of Kenyan communities up to the 19th Century"
                ]
            }
        },
        "CRE": {
            "Old Testament Leadership": {
                "Moses": [
                    "Explain the call and role of Moses in Israel's journey"
                ]
            }
        }
    },
    "Form 3": {
        "English": {
            "Functional Skills": {
                "Oral Communication": [
                    "Master mechanics of listening comprehension and speech delivery"
                ]
            }
        },
        "Mathematics": {
            "Calculus & Series": {
                "Sequences": [
                    "Find the nth term of an Arithmetic Progression (AP)"
                ]
            }
        },
        "Kiswahili": {
            "Sarufi na Matumizi ya Lugha": {
                "Ngeli za Nomino": [
                    "Kupanga nomino katika ngeli sahihi za Lugha ya Kiswahili"
                ]
            }
        },
        "Geography": {
            "Statistical Methods": {
                "Data Interpretation": [
                    "Draw and interpret statistical graphs and pie charts"
                ]
            }
        },
        "Physics": {
            "Waves": {
                "Light Reflection": [
                    "Apply laws of reflection to plane and curved mirrors"
                ]
            }
        },
        "Chemistry": {
            "Organic Chemistry": {
                "Alkanes": [
                    "Draw structures and write chemical properties of simple alkanes"
                ]
            }
        },
        "Biology": {
            "Ecology": {
                "Ecosystems": [
                    "Construct food chains and food webs within local habitats"
                ]
            }
        },
        "Business Studies": {
            "Finance": {
                "Financial Statements": [
                    "Prepare a clean Ledger, Balance Sheet, and Trial Balance"
                ]
            }
        },
        "History and Government": {
            "Political Developments": {
                "Colonial Administration": [
                    "Compare direct rule and indirect rule systems in Africa"
                ]
            }
        },
        "CRE": {
            "Prophets": {
                "Amos": [
                    "Analyze teachings of Prophet Amos on social justice and judgment"
                ]
            }
        }
    },
    "Form 4": {
        "English": {
            "Oral Skills": {
                "Poetry Interpretation": [
                    "Analyze rhythm, rhyme, and tone in spoken verse performance"
                ]
            }
        },
        "Mathematics": {
            "Matrices & Transformations": {
                "Matrix Operations": [
                    "Determine the determinant and inverse of a 2x2 matrix", 
                    "Use matrix inversion to solve equations"
                ]
            }
        },
        "Kiswahili": {
            "Insha": {
                "Insha za Kitaalamu": [
                    "Kuandika ripoti, wasifu, na kumbukumbu za mikutano rasmi"
                ]
            }
        },
        "Geography": {
            "Management & Conservation": {
                "Environment": [
                    "Identify environmental management actions to curb desertification"
                ]
            }
        },
        "Physics": {
            "Atomic Physics": {
                "Radioactivity": [
                    "Solve half-life calculations for radioactive isotopes", 
                    "Distinguish radiation emission particles"
                ]
            }
        },
        "Chemistry": {
            "Electrochemistry": {
                "Electrolysis": [
                    "Predict products of electrolysis in aqueous solutions and molten salts"
                ]
            }
        },
        "Biology": {
            "Genetics": {
                "Inheritance": [
                    "Predict monohybrid genetic crosses using Punnett squares"
                ]
            }
        },
        "Business Studies": {
            "International Trade": {
                "Balance of Payments": [
                    "Examine corrections for deficits in international balance systems"
                ]
            }
        },
        "History and Government": {
            "World History": {
                "International Relations": [
                    "Examine the formation, achievements, and challenges of the United Nations"
                ]
            }
        },
        "CRE": {
            "Christian Approaches": {
                "Work & Leisure": [
                    "Evaluate the Christian meaning of work and the misuse of leisure time"
                ]
            }
        }
    }
}