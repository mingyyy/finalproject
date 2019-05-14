import app_user.constants as cons
from app_user.models import Language, Topic

lan=[]
for x in cons.LANGUAGE_LIST:
    lan.append(Language(language=x))
print(lan)

topic=[]
for x in cons.SUBJECT_LIST:
    topic.append(Topic(topic=x))
print(topic)

SUBJECT_LIST = ['Accounting', 'Analytics', 'Assessing Performance', 'Auditing', 'Balanced Scorecard', 'Behavioral Economics',
                'Boards', 'Branding', 'Budgeting', 'Business Education', 'Business History', 'Business Law', 'Business Models',
                'Business Processes', 'Business Writing', 'Career Planning', 'Change Management', 'Coaching', 'Collaboration',
                'Communication', 'Compensation', 'Competition', 'Competitive Strategy', 'Conflict', 'Corporate Communications',
                'Corporate Governance', 'Costs', 'Creativity', 'Crisis Communication', 'Crisis Management',
                'Cross-Cultural Management', 'Currency', 'Customer Service', 'Customers', 'Data', 'Decision Making',
                'Delegation', 'Demographics', 'Design', 'Developing Employees', 'Difficult Conversations',
                'Disruptive Innovation', 'Diversity', 'Downsizing', 'Economic Development', 'Economics', 'Economics & Society',
                'Economy', 'Education', 'Emerging Markets', 'Emotional Intelligence', 'Employee Retention',
                'Entrepreneurial Finance', 'Entrepreneurial Management', 'Entrepreneurship', 'Ethics',
                'Executive Compensation', 'Experimentation', 'Finance & Accounting', 'Financial Analysis',
                'Financial Management', 'Financial Markets', 'Firing', 'Forecasting', 'Founders', 'Gender',
                'Generational Issues', 'Giving Feedback', 'Global Strategy', 'Globalization', 'Government', 'Growth Strategy',
                'Health', 'Hiring', 'Human Resource Management', 'Influence', 'Informal Leadership', 'Innovation',
                'Intellectual Property', 'International Business', 'Internet', 'IPO', 'IT', 'Job Search', 'Joint Ventures',
                'Knowledge Management', 'Labor', 'Leadership', 'Leadership & Managing People', 'Leadership Development',
                'Leadership Transitions', 'Leading Teams', 'Managing Organizations', 'Managing People', 'Managing Uncertainty',
                'Managing Up', 'Managing Yourself', 'Manufacturing', 'Market Research', 'Marketing', 'Meetings',
                'Mergers & Acquisitions', 'Mobile', 'Motivating People', 'National Competitiveness', 'Negotiations',
                'Networking', 'Operations', 'Operations Management', 'Organizational Culture', 'Organizational Structure',
                'Performance Measurement', 'Personnel Policies', 'Policy', 'Presentations', 'Pricing', 'Product Development',
                'Productivity', 'Professional Transitions', 'Project Management', 'Psychology', 'Public Relations',
                'Public-Private Partnerships', 'Race', 'Receiving Feedback', 'Recession', 'Regulation', 'Reorganization',
                'Research & Development', 'Retirement', 'Risk Management', 'Sales', 'Sales & Marketing', 'Security & Privacy',
                'Sexual Orientation', 'Shared Value', 'Social Enterprise', 'Social Platforms', 'Social Responsibility',
                'Strategic Planning', 'Strategic Thinking', 'Strategy', 'Strategy Execution', 'Stress', 'Succession Planning',
                'Supply Chain', 'Sustainability', 'Talent Management', 'Technology', 'Time Management', 'Transparency',
                'Venture Capital', 'Work-Life Balance', 'Workspaces']

