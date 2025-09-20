import os
import json
import requests
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import re
import time

app = Flask(__name__)

# Global variables to store data
all_candidates = []
user_added_candidates = []

def load_candidates():
    """Load candidates from the applications.json file"""
    global all_candidates
    try:
        # Try to load from the specified path first
        with open('applications.json', 'r', encoding='utf-8') as f:
            all_candidates = json.load(f)
        print(f"Loaded {len(all_candidates)} candidates from applications.json")
    except FileNotFoundError:
        # Fallback to a sample dataset for demo purposes
        print("Warning: applications.json not found. Using sample data.")
        all_candidates = [
            {
                "name": "Clever Monkey",
                "email": "clever-monkey@example.com",
                "phone": "5582981474204",
                "location": "Maceió",
                "submitted_at": "2025-01-28 09:02:16.000000",
                "work_availability": [
                    "full-time",
                    "part-time"
                ],
                "annual_salary_expectation": {
                    "full-time": "$117548"
                },
                "work_experiences": [
                    {
                        "company": "StarLab Digital Ventures",
                        "roleName": "Full Stack Developer"
                    },
                    {
                        "company": "OrbitalLife",
                        "roleName": "Project Manager"
                    },
                    {
                        "company": "Carrot Hosting",
                        "roleName": "Full Stack Developer"
                    },
                    {
                        "company": "Bitbay Solutions",
                        "roleName": "Full Stack Developer"
                    },
                    {
                        "company": "Federal Institute of Science, Education & Technology - Alagoas",
                        "roleName": "Project Manager"
                    },
                    {
                        "company": "Usina Caeté",
                        "roleName": "Scientist"
                    },
                    {
                        "company": "Cyberia",
                        "roleName": "System Administrator"
                    }
                ],
                "education": {
                    "highest_level": "Bachelor's Degree",
                    "degrees": [
                        {
                            "degree": "Bachelor's Degree",
                            "subject": "Computer Science",
                            "school": "International Institutions",
                            "gpa": "GPA 3.0-3.4",
                            "startDate": "2023",
                            "endDate": "2027",
                            "originalSchool": "Faculdade Descomplica",
                        },
                        {
                            "degree": "Bachelor's Degree",
                            "subject": "Law",
                            "school": "International Institutions",
                            "gpa": "GPA 3.0-3.4",
                            "startDate": "2015",
                            "endDate": "2023",
                            "originalSchool": "Federal University of Alagoas",
                        },
                        {
                            "degree": "Bachelor's Degree",
                            "subject": "Chemistry",
                            "school": "International Institutions",
                            "gpa": "GPA 3.0-3.4",
                            "startDate": "2011",
                            "endDate": "2014",
                            "originalSchool": "Federal Institute of Alagoas",
                        }
                    ]
                },
                "skills": [
                    "Data Analysis",
                    "Docker",
                    "Microservices"
                ]
            },
            {
                "name": "Noble Flamingo",
                "email": "noble-flamingo@example.com",
                "phone": "12156688210",
                "location": "Philadelphia",
                "submitted_at": "2025-01-26 07:40:39.000000",
                "work_availability": [
                    "full-time",
                    "part-time"
                ],
                "annual_salary_expectation": {
                    "full-time": "$112253"
                },
                "work_experiences": [
                    {
                        "company": "Intellectual Asset Management Group",
                        "roleName": "Managing Director"
                    },
                    {
                        "company": "Raju LLP",
                        "roleName": "Partner"
                    },
                    {
                        "company": "Angeion Group",
                        "roleName": "Legal Specialist"
                    },
                    {
                        "company": "Unilog Corporation",
                        "roleName": "Legal Specialist"
                    },
                    {
                        "company": "Spruce Law",
                        "roleName": "Legal Specialist"
                    },
                    {
                        "company": "Newport IP",
                        "roleName": "Legal Specialist"
                    },
                    {
                        "company": "Knox Investment Group",
                        "roleName": "Managing Director"
                    },
                    {
                        "company": "Drinker Biddle & Reath",
                        "roleName": "Attorney"
                    }
                ],
                "education": {
                    "highest_level": "Juris Doctor (J.D)",
                    "degrees": [
                        {
                            "degree": "Master's Degree",
                            "subject": "Accounting",
                            "school": "Top Schools",
                            "gpa": "GPA 3.5-3.9",
                            "startDate": "2005",
                            "endDate": "2006",
                            "originalSchool": "The Wharton School",
                        },
                        {
                            "degree": "Juris Doctor (J.D)",
                            "subject": "",
                            "school": "Top Private Universities",
                            "gpa": "GPA 3.5-3.9",
                            "startDate": "",
                            "endDate": "1999",
                            "originalSchool": "Pepperdine University School of Law",
                        },
                        {
                            "degree": "Bachelor's Degree",
                            "subject": "Electrical Engineering",
                            "school": "Top Schools",
                            "gpa": "GPA 3.5-3.9",
                            "startDate": "",
                            "endDate": "1995",
                            "originalSchool": "University of Pennsylvania",
                        }
                    ]
                },
                "skills": []
            },
            {
                "name": "Noble Antelope",
                "email": "noble-antelope@example.com",
                "phone": "8801993762548",
                "location": "Bangladesh",
                "submitted_at": "2025-01-28 07:29:47.000000",
                "work_availability": [
                    "full-time",
                    "part-time"
                ],
                "annual_salary_expectation": {
                    "full-time": "$63556"
                },
                "work_experiences": [
                    {
                        "company": "Red.Digital",
                        "roleName": "Software Engineer"
                    },
                    {
                        "company": "Robi-HRIS SaaS Product",
                        "roleName": "Software Engineer"
                    },
                    {
                        "company": "Dotlines",
                        "roleName": "Software Engineer"
                    },
                    {
                        "company": "BJIT Group",
                        "roleName": "Software Engineer"
                    }
                ],
                "education": {
                    "highest_level": "Bachelor's Degree",
                    "degrees": [
                        {
                            "degree": "Bachelor's Degree",
                            "subject": "Computer Science",
                            "school": "International Institutions",
                            "gpa": "GPA 3.5-3.9",
                            "startDate": "2016",
                            "endDate": "2021",
                            "originalSchool": "Chittagong University of Engineering & Technology",
                        },
                        {
                            "degree": "High School Diploma",
                            "subject": "",
                            "school": "State Universities",
                            "gpa": "GPA 3.0-3.4",
                            "startDate": "2013",
                            "endDate": "2015",
                            "originalSchool": "Govt Hazi Mohammed Mohsin College",
                        }
                    ]
                },
                "skills": [
                    "Laravel",
                    "Next JS",
                    "React",
                    "React Native",
                    "Redux",
                    "Angular"
                ]
            },
            {
                "name": "Quantum Eagle",
                "email": "quantum-eagle@example.com",
                "phone": "15551234567",
                "location": "San Francisco, CA",
                "submitted_at": "2025-01-29 10:15:30.000000",
                "work_availability": [
                    "full-time",
                    "part-time"
                ],
                "annual_salary_expectation": {
                    "full-time": "$145000"
                },
                "work_experiences": [
                    {
                        "company": "NeuralTech AI",
                        "roleName": "AI Engineer"
                    },
                    {
                        "company": "DeepMind Solutions",
                        "roleName": "Machine Learning Engineer"
                    },
                    {
                        "company": "Stanford AI Lab",
                        "roleName": "Research Assistant"
                    },
                    {
                        "company": "Google Brain",
                        "roleName": "AI Developer"
                    }
                ],
                "education": {
                    "highest_level": "PhD",
                    "degrees": [
                        {
                            "degree": "PhD",
                            "subject": "Computer Science - AI",
                            "school": "Top Schools",
                            "gpa": "GPA 3.9-4.0",
                            "startDate": "2018",
                            "endDate": "2023",
                            "originalSchool": "Stanford University",
                        },
                        {
                            "degree": "Master's Degree",
                            "subject": "Machine Learning",
                            "school": "Top Schools",
                            "gpa": "GPA 3.9-4.0",
                            "startDate": "2016",
                            "endDate": "2018",
                            "originalSchool": "Stanford University",
                        }
                    ]
                },
                "skills": [
                    "Python",
                    "TensorFlow",
                    "PyTorch",
                    "Machine Learning",
                    "Deep Learning",
                    "Computer Vision",
                    "NLP",
                    "Neural Networks"
                ]
            },
            {
                "name": "Data Phoenix",
                "email": "data-phoenix@example.com",
                "phone": "14155556789",
                "location": "Seattle, WA",
                "submitted_at": "2025-01-28 14:22:45.000000",
                "work_availability": [
                    "full-time"
                ],
                "annual_salary_expectation": {
                    "full-time": "$135000"
                },
                "work_experiences": [
                    {
                        "company": "Amazon AI",
                        "roleName": "Data Scientist"
                    },
                    {
                        "company": "Microsoft Research",
                        "roleName": "AI Research Engineer"
                    },
                    {
                        "company": "Tesla AI",
                        "roleName": "Autonomous Systems Engineer"
                    }
                ],
                "education": {
                    "highest_level": "Master's Degree",
                    "degrees": [
                        {
                            "degree": "Master's Degree",
                            "subject": "Data Science",
                            "school": "Top Schools",
                            "gpa": "GPA 3.7-3.9",
                            "startDate": "2017",
                            "endDate": "2019",
                            "originalSchool": "University of Washington",
                        },
                        {
                            "degree": "Bachelor's Degree",
                            "subject": "Computer Science",
                            "school": "Top Schools",
                            "gpa": "GPA 3.7-3.9",
                            "startDate": "2013",
                            "endDate": "2017",
                            "originalSchool": "University of Washington",
                        }
                    ]
                },
                "skills": [
                    "Python",
                    "R",
                    "SQL",
                    "Machine Learning",
                    "Data Analysis",
                    "Statistics",
                    "AWS",
                    "Spark"
                ]
            },
            {
                "name": "Cyber Wolf",
                "email": "cyber-wolf@example.com",
                "phone": "12025554321",
                "location": "Boston, MA",
                "submitted_at": "2025-01-27 16:30:12.000000",
                "work_availability": [
                    "full-time",
                    "contract"
                ],
                "annual_salary_expectation": {
                    "full-time": "$125000"
                },
                "work_experiences": [
                    {
                        "company": "OpenAI",
                        "roleName": "NLP Engineer"
                    },
                    {
                        "company": "IBM Watson",
                        "roleName": "AI Developer"
                    },
                    {
                        "company": "MIT CSAIL",
                        "roleName": "Research Engineer"
                    }
                ],
                "education": {
                    "highest_level": "Master's Degree",
                    "degrees": [
                        {
                            "degree": "Master's Degree",
                            "subject": "Natural Language Processing",
                            "school": "Top Schools",
                            "gpa": "GPA 3.8-4.0",
                            "startDate": "2019",
                            "endDate": "2021",
                            "originalSchool": "MIT",
                        },
                        {
                            "degree": "Bachelor's Degree",
                            "subject": "Linguistics",
                            "school": "Top Schools",
                            "gpa": "GPA 3.5-3.9",
                            "startDate": "2015",
                            "endDate": "2019",
                            "originalSchool": "Harvard University",
                        }
                    ]
                },
                "skills": [
                    "Python",
                    "NLP",
                    "Transformers",
                    "BERT",
                    "GPT",
                    "Machine Learning",
                    "Deep Learning",
                    "Natural Language Processing"
                ]
            }
        ]
    except Exception as e:
        print(f"Error loading candidates: {e}")
        all_candidates = []

def normalize_position(position):
    """Normalize position string for matching"""
    return position.strip().lower().replace('-', ' ')

def get_position_synonyms(position):
    """Get synonyms for common position types"""
    synonyms_map = {
        'full stack': ['fullstack', 'full-stack', 'software engineer', 'software developer'],
        'fullstack': ['full stack', 'full-stack', 'software engineer', 'software developer'],
        'backend': ['back-end', 'back end', 'server side', 'api developer'],
        'frontend': ['front-end', 'front end', 'ui developer', 'web developer'],
        'software engineer': ['developer', 'programmer', 'software developer'],
        'ai': ['artificial intelligence', 'machine learning', 'ml', 'deep learning', 'neural network', 'computer vision', 'nlp', 'natural language processing'],
        'machine learning': ['ml', 'artificial intelligence', 'ai', 'deep learning', 'neural network', 'data science'],
        'data science': ['data scientist', 'machine learning', 'ml', 'ai', 'artificial intelligence', 'analytics', 'data analysis'],
        'developer': ['engineer', 'programmer', 'software developer', 'coder'],
        'engineer': ['developer', 'software engineer', 'technical engineer'],
    }
    
    normalized = normalize_position(position)
    synonyms = []
    
    for key, values in synonyms_map.items():
        if key in normalized:
            synonyms.extend(values)
    
    return synonyms

def score_candidate(candidate, position_keywords):
    """Calculate match score for a candidate (0-100)"""
    score = 0
    
    # Experience title match (60% weight)
    experience_score = 0
    for exp in candidate.get('work_experiences', []):
        role_name = exp.get('roleName', '').lower()
        for keyword in position_keywords:
            if keyword in role_name:
                if keyword == normalize_position(' '.join(position_keywords)):
                    experience_score = 100  # Exact match
                    break
                else:
                    experience_score = max(experience_score, 80)  # Partial match
    
    # Skills match (30% weight)
    skills_score = 0
    candidate_skills = [skill.lower() for skill in candidate.get('skills', [])]
    matching_skills = sum(1 for keyword in position_keywords if any(keyword in skill for skill in candidate_skills))
    if position_keywords:
        skills_score = (matching_skills / len(position_keywords)) * 100
    
    # Education bonus (10% weight)
    education_score = 0
    education_data = candidate.get('education', {})
    if isinstance(education_data, dict):
        # Handle new education structure
        highest_level = education_data.get('highest_level', '').lower()
        degrees = education_data.get('degrees', [])

        if 'master' in highest_level or 'phd' in highest_level or 'juris doctor' in highest_level:
            education_score = 10
        elif 'bachelor' in highest_level:
            education_score = 5

        # Check degrees for top institutions
        for degree in degrees:
            institution = degree.get('originalSchool', '').lower()
            if any(top_school in institution for top_school in ['stanford', 'mit', 'harvard', 'berkeley', 'pennsylvania', 'wharton']):
                education_score += 5
                break
    else:
        # Handle old education structure (array)
        for edu in education_data:
            degree = edu.get('degree', '').lower()
            institution = edu.get('institution', '').lower()
            if 'master' in degree or 'phd' in degree:
                education_score = 10
            elif 'bachelor' in degree:
                education_score = 5

            # Bonus for top institutions
            if any(top_school in institution for top_school in ['stanford', 'mit', 'harvard', 'berkeley']):
                education_score += 5

    # Calculate final score
    final_score = (experience_score * 0.6) + (skills_score * 0.3) + (education_score * 0.1)

    # Small penalty for high salary expectations (prefer lower when similar)
    salary_data = candidate.get('annual_salary_expectation', {})
    if isinstance(salary_data, dict):
        # Handle salary as object with full-time/part-time
        full_time_salary = salary_data.get('full-time', '0').replace('$', '').replace(',', '')
        try:
            salary = int(full_time_salary)
        except ValueError:
            salary = 100000
    else:
        # Handle salary as direct number
        salary = salary_data if isinstance(salary_data, (int, float)) else 100000

    if salary > 150000:
        final_score -= 5
    
    return min(100, max(0, final_score))

def filter_candidates(position):
    """Filter candidates based on position requirements"""
    if not position:
        return []

    normalized_position = normalize_position(position)
    position_keywords = normalized_position.split()
    synonyms = get_position_synonyms(position)
    all_keywords = position_keywords + synonyms

    filtered = []
    seen_candidates = set()

    # Combine all candidates (loaded + user added)
    all_current_candidates = all_candidates + user_added_candidates

    for candidate in all_current_candidates:
        # Check for duplicates by email or name+phone
        identifier = candidate.get('email') or f"{candidate.get('name', '')}_{candidate.get('phone', '')}"
        if identifier in seen_candidates:
            continue
        seen_candidates.add(identifier)

        matches = False

        # Check work experience role names
        for exp in candidate.get('work_experiences', []):
            role_name = exp.get('roleName', '').lower()
            # Check if any keyword is exactly equal to role_name or contained in role_name
            for keyword in all_keywords:
                if keyword == role_name or keyword in role_name:
                    matches = True
                    break
            if matches:
                break

        # Check skills
        if not matches:
            candidate_skills = [skill.lower() for skill in candidate.get('skills', [])]
            if any(keyword in ' '.join(candidate_skills) for keyword in position_keywords):
                matches = True

        if matches:
            # Calculate match score
            match_score = score_candidate(candidate, position_keywords)
            candidate_copy = candidate.copy()
            candidate_copy['match_score'] = match_score
            filtered.append(candidate_copy)

    # Sort by match score descending
    filtered.sort(key=lambda x: x['match_score'], reverse=True)

    return filtered

def check_gemini_availability():
    """Check if Gemini API is available and working"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return False, "GEMINI_API_KEY environment variable not set"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": "Hello, this is a test message to check API availability."}
                        ]
                    }
                ]
            }

            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                return True, "Gemini API is available"
            else:
                return False, f"Gemini API returned status code: {response.status_code}"

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Timeout on attempt {attempt + 1}, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return False, "Network timeout after multiple retries"
        except requests.exceptions.RequestException as e:
            return False, f"Network error connecting to Gemini API: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error with Gemini API: {str(e)}"
    # Ensure a tuple is always returned
    return False, "Unknown error checking Gemini API"

def call_gemini(filtered_candidates, job_title):
    """Call Gemini API to rank candidates"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    # Limit to top 20 candidates if too many
    candidates_to_send = filtered_candidates[:20] if len(filtered_candidates) > 20 else filtered_candidates
    truncated = len(filtered_candidates) > 20
    
    system_message = """You are an expert hiring analyst. Given a list of candidate profiles in JSON, rank them from best fit to worst fit for the job title provided. Produce a strict JSON response using the 'ranked_candidates' array schema described below. Be concise but explicit. Explain strengths and weaknesses for the top 3 and bottom 2. Use hiring criteria including relevant experience (roleName), measurable skills, recency of experience, breadth (front+back), and value (salary expectation). Avoid hallucinations: only use the data provided in the JSON. If any information is missing, say so explicitly in candidate reason."""
    
    filter_reason = f"Filtered by role name and skills matching '{job_title}'. Found {len(filtered_candidates)} matches."
    if truncated:
        filter_reason += f" Showing top 20 by match_score."
    
    user_message = {
        "job_title": job_title,
        "filter_reason": filter_reason,
        "candidates": candidates_to_send
    }
    
    # Gemini API call
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"SYSTEM: {system_message}\n\nUSER: {json.dumps(user_message)}\n\nRespond with JSON only in this exact format:\n{{\n  \"job_title\": \"<same string>\",\n  \"ranked_candidates\": [\n    {{\n      \"rank\": 1,\n      \"name\": \"<name>\",\n      \"email\": \"<email or null>\",\n      \"match_score\": <0-100 numeric>,\n      \"final_score\": <0-100 numeric>,\n      \"strengths\": [\"short bullet 1\", \"short bullet 2\"],\n      \"weaknesses\": [\"short bullet 1\"],\n      \"why_on_top\": \"<1-2 sentence reason>\",\n      \"why_on_bottom\": \"<1-2 sentence reason (for bottom-most only)>\"\n    }}\n  ],\n  \"chosen_for_hire\": [\"email-of-5-selected\"],\n  \"selection_reasoning\": \"<1 paragraph explaining why those 5>\"\n}}"}
                ]
            }
        ]
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()

            # Extract the generated text
            if 'candidates' in result and len(result['candidates']) > 0:
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
            else:
                raise ValueError("Unexpected Gemini API response format")

            # Try to parse JSON from the response
            try:
                # Look for JSON in the response
                json_start = generated_text.find('{')
                json_end = generated_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_text = generated_text[json_start:json_end]
                    return json.loads(json_text)
                else:
                    raise ValueError("No JSON found in Gemini response")
            except json.JSONDecodeError:
                # Fallback: create a simple ranking based on match_score
                ranked_candidates = []
                for i, candidate in enumerate(candidates_to_send[:5]):
                    ranked_candidates.append({
                        "rank": i + 1,
                        "name": candidate['name'],
                        "email": candidate.get('email'),
                        "match_score": candidate['match_score'],
                        "final_score": candidate['match_score'],
                        "strengths": ["High match score", "Relevant experience"],
                        "weaknesses": ["Limited information available"],
                        "why_on_top": "Strong technical match for the position" if i < 3 else "",
                        "why_on_bottom": "Lower overall match score" if i >= len(candidates_to_send) - 2 else ""
                    })

                return {
                    "job_title": job_title,
                    "ranked_candidates": ranked_candidates,
                    "chosen_for_hire": [c.get('email', c['name']) for c in candidates_to_send[:5]],
                    "selection_reasoning": "Selected top 5 candidates based on match scores and technical fit."
                }

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Timeout on attempt {attempt + 1}, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise Exception("Network timeout after multiple retries")
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Return fallback ranking
            ranked_candidates = []
            for i, candidate in enumerate(candidates_to_send[:5]):
                ranked_candidates.append({
                    "rank": i + 1,
                    "name": candidate['name'],
                    "email": candidate.get('email'),
                    "match_score": candidate['match_score'],
                    "final_score": candidate['match_score'],
                    "strengths": ["Technical skills match", "Relevant experience"],
                    "weaknesses": ["API unavailable for detailed analysis"],
                    "why_on_top": "High match score and relevant background" if i < 3 else "",
                    "why_on_bottom": "Lower technical match" if i >= len(candidates_to_send) - 2 else ""
                })

            return {
                "job_title": job_title,
                "ranked_candidates": ranked_candidates,
                "chosen_for_hire": [c.get('email', c['name']) for c in candidates_to_send[:5]],
                "selection_reasoning": f"Fallback ranking due to API error: {str(e)}"
            }

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/candidates')
def get_all_candidates():
    """Get all candidate names for the scrolling ticker"""
    all_names = []
    
    # Add names from loaded candidates
    for candidate in all_candidates:
        all_names.append(candidate.get('name', 'Unknown'))
    
    # Add names from user-added candidates
    for candidate in user_added_candidates:
        all_names.append(candidate.get('name', 'Unknown'))
    
    return jsonify(all_names)

@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    """Add a new candidate manually"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # Create candidate object
    candidate = {
        'name': data['name'],
        'email': data.get('email', ''),
        'phone': data.get('phone', ''),
        'location': data.get('location', ''),
        'submitted_at': datetime.now().isoformat() + 'Z',
        'work_experiences': [],
        'education': [],
        'skills': [skill.strip() for skill in data.get('skills', '').split(',') if skill.strip()],
        'annual_salary_expectation': data.get('salary', 0)
    }
    
    user_added_candidates.append(candidate)
    return jsonify({'success': True, 'candidate': candidate})

@app.route('/filter', methods=['POST'])
def filter_candidates_endpoint():
    """Filter candidates based on position"""
    data = request.get_json()
    position = data.get('position', '')
    
    if not position:
        return jsonify({'error': 'Position is required'}), 400
    
    filtered = filter_candidates(position)
    
    # Save sample filtered results
    if position.lower().replace('-', ' ') == 'fullstack developer':
        with open('sample_filtered.json', 'w') as f:
            json.dump({
                'position': position,
                'candidates': filtered,
                'count': len(filtered)
            }, f, indent=2)
    
    return jsonify({
        'position': position,
        'candidates': filtered,
        'count': len(filtered)
    })

@app.route('/rank', methods=['POST'])
def rank_candidates():
    """Rank filtered candidates using Gemini"""
    data = request.get_json()

    if 'candidates' not in data:
        return jsonify({'error': 'Candidates list is required'}), 400

    job_title = data.get('job_title') or data.get('position', 'Unknown Position')
    candidates = data['candidates']

    # Check Gemini availability first
    gemini_available, gemini_message = check_gemini_availability()

    if not gemini_available:
        print(f"Gemini not available: {gemini_message}")
        # Provide fallback ranking based on match_score
        ranked_candidates = []
        for i, candidate in enumerate(candidates[:5]):
            ranked_candidates.append({
                "rank": i + 1,
                "name": candidate['name'],
                "email": candidate.get('email'),
                "match_score": candidate.get('match_score', 0),
                "final_score": candidate.get('match_score', 0),
                "strengths": ["Technical skills match position requirements", "Relevant experience"],
                "weaknesses": ["Gemini AI ranking unavailable - using basic scoring"],
                "why_on_top": "Highest match score for the position" if i < 3 else "",
                "why_on_bottom": "Lower technical match score" if i >= len(candidates) - 2 else ""
            })

        fallback_result = {
            "job_title": job_title,
            "ranked_candidates": ranked_candidates,
            "chosen_for_hire": [c.get('email', c['name']) for c in candidates[:5]],
            "selection_reasoning": f"Fallback ranking due to Gemini API unavailability: {gemini_message}. Selected top candidates based on match scores.",
            "gemini_available": False,
            "fallback_used": True
        }

        # Save sample ranked results
        if job_title.lower().replace('-', ' ') == 'ai developer':
            with open('sample_ranked.json', 'w') as f:
                json.dump(fallback_result, f, indent=2)

        return jsonify(fallback_result)

    try:
        ranked_result = call_gemini(candidates, job_title)
        ranked_result['gemini_available'] = True
        ranked_result['fallback_used'] = False

        # Save sample ranked results
        if job_title.lower().replace('-', ' ') == 'ai developer':
            with open('sample_ranked.json', 'w') as f:
                json.dump(ranked_result, f, indent=2)

        return jsonify(ranked_result)

    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback to basic ranking
        ranked_candidates = []
        for i, candidate in enumerate(candidates[:5]):
            ranked_candidates.append({
                "rank": i + 1,
                "name": candidate['name'],
                "email": candidate.get('email'),
                "match_score": candidate.get('match_score', 0),
                "final_score": candidate.get('match_score', 0),
                "strengths": ["Technical skills match position requirements", "Relevant experience"],
                "weaknesses": [f"Gemini API error: {str(e)}"],
                "why_on_top": "Highest match score for the position" if i < 3 else "",
                "why_on_bottom": "Lower technical match score" if i >= len(candidates) - 2 else ""
            })

        error_result = {
            "job_title": job_title,
            "ranked_candidates": ranked_candidates,
            "chosen_for_hire": [c.get('email', c['name']) for c in candidates[:5]],
            "selection_reasoning": f"Error with Gemini API: {str(e)}. Using fallback ranking based on match scores.",
            "gemini_available": False,
            "fallback_used": True,
            "error": str(e)
        }

        return jsonify(error_result)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    api_key_set = bool(os.getenv('GEMINI_API_KEY'))
    gemini_available, gemini_message = check_gemini_availability()
    return jsonify({
        'status': 'healthy',
        'candidates_loaded': len(all_candidates),
        'gemini_api_key_set': api_key_set,
        'gemini_available': gemini_available,
        'gemini_status': gemini_message
    })

@app.route('/check_gemini')
def check_gemini_endpoint():
    """Check Gemini API availability"""
    available, message = check_gemini_availability()
    return jsonify({
        'available': available,
        'message': message
    })

@app.route('/debug_filter/<position>')
def debug_filter(position):
    """Debug endpoint to test filtering logic"""
    normalized_position = normalize_position(position)
    position_keywords = normalized_position.split()
    synonyms = get_position_synonyms(position)
    all_keywords = position_keywords + synonyms

    debug_info = {
        'position': position,
        'normalized_position': normalized_position,
        'position_keywords': position_keywords,
        'synonyms': synonyms,
        'all_keywords': all_keywords,
        'total_candidates': len(all_candidates),
        'candidates': []
    }

    for candidate in all_candidates:
        candidate_info = {
            'name': candidate.get('name'),
            'work_experiences': [exp.get('roleName') for exp in candidate.get('work_experiences', [])],
            'skills': candidate.get('skills', []),
            'matches': False
        }

        # Check work experience role names
        for exp in candidate.get('work_experiences', []):
            role_name = exp.get('roleName', '').lower()
            for keyword in all_keywords:
                if keyword == role_name or keyword in role_name:
                    candidate_info['matches'] = True
                    break
            if candidate_info['matches']:
                break

        # Check skills if not matched by experience
        if not candidate_info['matches']:
            candidate_skills = [skill.lower() for skill in candidate.get('skills', [])]
            if any(keyword in ' '.join(candidate_skills) for keyword in position_keywords):
                candidate_info['matches'] = True

        debug_info['candidates'].append(candidate_info)

    return jsonify(debug_info)

if __name__ == '__main__':
    # Load candidates on startup
    load_candidates()
    
    # Check for API key
    if not os.getenv('GEMINI_API_KEY'):
        print("WARNING: GEMINI_API_KEY environment variable not set!")
        print("Set it with: export GEMINI_API_KEY=your_api_key_here")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
