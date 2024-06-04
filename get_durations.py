import re
from datetime import datetime

def parse_dates(text):
    try:
        date_patterns = [
            r'\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.? (\d{4})\b',
            r'\b(\d{4})\b'
        ]
        
        # Extract dates matching the patterns
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    month_str, year = match
                    month = datetime.strptime(month_str[:3], '%b').month
                    dates.append((int(year), month))
                elif len(match) == 1:
                    year = match[0]
                    dates.append((int(year), None))

        # Sort dates based on year and month
        dates.sort(key=lambda date: (date[0], date[1] if date[1] else 0))
    except Exception as e:
        print(e)
    return dates

def calculate_career_duration(dates):
    if not dates:
        return 0, False, []
    
    # Calculate total career duration and gaps
    start_year, start_month = dates[0]
    end_year, end_month = dates[-1]
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    if end_month is None:
        end_month = 12
    
    total_years = end_year - start_year
    total_months = end_month - start_month if end_month >= start_month else 12 + end_month - start_month - 1
    
    if end_year == start_year:
        total_duration = total_months / 12.0
    else:
        total_duration = total_years + total_months / 12.0
    
    is_still_working = (end_year == current_year and end_month >= current_month) or (end_year > current_year)

    # Calculate gaps between jobs
    gaps = []
    for i in range(1, len(dates)):
        prev_year, prev_month = dates[i-1]
        curr_year, curr_month = dates[i]
        
        if prev_month is None:
            prev_month = 12
        if curr_month is None:
            curr_month = 1
        
        gap_years = curr_year - prev_year
        gap_months = curr_month - prev_month if curr_month >= prev_month else 12 + curr_month - prev_month - 1
        
        if gap_years > 0 or gap_months > 0:
            gaps.append((gap_years, gap_months))
    
    return total_duration, is_still_working, gaps

def get_durations(resume_text):
    dates = parse_dates(resume_text)
    career_duration, is_still_working, gaps = calculate_career_duration(dates)
    
    # Convert career duration into years and months
    career_years = int(career_duration)
    career_months = int((career_duration - career_years) * 12)
    
    # Convert gaps into readable format
    gap_durations = []
    for years, months in gaps:
        total_months = years * 12 + months
        gap_years = total_months // 12
        gap_months = total_months % 12
        gap_durations.append(f"{gap_years} years and {gap_months} months" if gap_years else f"{gap_months} months")
    
    # Format career duration
    career_duration_str = f"{career_years} years and {career_months} months" if career_years else f"{career_months} months"
    
    return career_duration_str, is_still_working, gap_durations