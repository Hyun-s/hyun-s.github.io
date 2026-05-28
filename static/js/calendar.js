// static/js/calendar.js

class JobCalendar {
    constructor(jobs, categories) {
        this.jobs = jobs || [];
        this.categories = this._indexCategories(categories || []);
        this.currentDate = new Date();
        this.activeFilters = new Set();
        this.searchQuery = '';
        
        this._init();
    }
    
    _indexCategories(categories) {
        const indexed = {};
        categories.forEach(cat => {
            indexed[cat.slug] = cat;
        });
        return indexed;
    }
    
    _init() {
        this._renderCalendar();
        this._setupEventListeners();
    }
    
    _setupEventListeners() {
        // Month navigation
        document.getElementById('prev-month').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this._renderCalendar();
        });
        
        document.getElementById('next-month').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this._renderCalendar();
        });

        // Search input
        document.getElementById('job-search').addEventListener('input', (e) => {
            this.searchQuery = e.target.value.toLowerCase();
            this._renderCalendar();
        });
        
        // Category filters
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const category = e.target.dataset.category;
                
                // toggle visual active state
                if(category === 'all') {
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                } else {
                    document.querySelector('[data-category="all"]').classList.remove('active');
                    e.target.classList.toggle('active');
                }

                this._toggleFilter(category);
            });
        });
        
        // Modal closing
        document.querySelector('.close-modal').addEventListener('click', () => {
            document.getElementById('job-modal').style.display = 'none';
        });
        window.addEventListener('click', (e) => {
            if (e.target == document.getElementById('job-modal')) {
                document.getElementById('job-modal').style.display = 'none';
            }
        });
    }
    
    _renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Update header
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December'];
        document.getElementById('current-month').textContent = 
            `${monthNames[month]} ${year}`;
        
        // Generate calendar grid
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDay = firstDay.getDay();
        
        const daysContainer = document.getElementById('calendar-days');
        daysContainer.innerHTML = '';
        
        // Empty cells for days before month starts
        for (let i = 0; i < startingDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'calendar-day empty';
            daysContainer.appendChild(emptyCell);
        }
        
        // Filter jobs based on active categories and search query
        const filteredJobs = this.jobs.filter(job => {
            const matchesCategory = this.activeFilters.size === 0 || this.activeFilters.has(job.category);
            const matchesSearch = !this.searchQuery || 
                                 job.company.toLowerCase().includes(this.searchQuery) || 
                                 job.position.toLowerCase().includes(this.searchQuery);
            return matchesCategory && matchesSearch;
        });

        // Days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const dayCell = this._createDayCell(dateStr, day, filteredJobs);
            daysContainer.appendChild(dayCell);
        }
    }
    
    _createDayCell(dateStr, day, jobsToConsider) {
        const dayCell = document.createElement('div');
        dayCell.className = 'calendar-day';
        dayCell.dataset.date = dateStr;
        
        const dayNumber = document.createElement('span');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;
        dayCell.appendChild(dayNumber);
        
        // Find jobs for this date
        const jobsForDay = this._getJobsForDate(dateStr, jobsToConsider);
        
        if (jobsForDay.length > 0) {
            const chipsContainer = document.createElement('div');
            chipsContainer.className = 'job-chips';
            
            jobsForDay.forEach(job => {
                const chip = this._createJobChip(job);
                chipsContainer.appendChild(chip);
            });
            
            dayCell.appendChild(chipsContainer);
        }
        
        return dayCell;
    }
    
    _getJobsForDate(dateStr, jobs) {
        return jobs.filter(job => {
            // Check if date falls within job's recruitment period
            return dateStr >= job.start_date && dateStr <= job.end_date;
        });
    }
    
    _createJobChip(job) {
        const chip = document.createElement('div');
        chip.className = 'job-chip';
        chip.dataset.jobId = job.id;
        
        const category = this.categories[job.category];
        const color = category ? category.color : '#6B7280';
        
        chip.style.borderColor = color;
        chip.style.borderLeft = `3px solid ${color}`;
        
        const company = document.createElement('div');
        company.className = 'chip-company';
        company.textContent = job.company;
        
        const position = document.createElement('div');
        position.className = 'chip-position';
        position.textContent = job.position;
        
        const categoryBadge = document.createElement('span');
        categoryBadge.className = 'chip-category';
        categoryBadge.style.backgroundColor = color;
        categoryBadge.textContent = category ? category.name : job.category;
        
        chip.appendChild(company);
        chip.appendChild(position);
        chip.appendChild(categoryBadge);
        
        // Check for approaching deadline
        const endDate = new Date(job.end_date);
        // Normalize today to start of day
        const today = new Date();
        today.setHours(0,0,0,0);
        const daysUntilDeadline = Math.ceil((endDate - today) / (1000 * 60 * 60 * 24));
        
        if (daysUntilDeadline >= 0 && daysUntilDeadline <= 3) {
            chip.classList.add('urgent');
            chip.title = `Deadline: ${daysUntilDeadline} day(s) left!`;
        }
        
        chip.addEventListener('click', (e) => {
            e.stopPropagation();
            this._showJobModal(job.id);
        });

        return chip;
    }
    
    _toggleFilter(category) {
        if (category === 'all') {
            this.activeFilters.clear();
        } else {
            if (this.activeFilters.has(category)) {
                this.activeFilters.delete(category);
            } else {
                this.activeFilters.add(category);
            }
        }
        this._renderCalendar();
    }
    
    _showJobModal(jobId) {
        const job = this.jobs.find(j => j.id === jobId);
        if(!job) return;

        document.getElementById('modal-company').textContent = job.company;
        document.getElementById('modal-position').textContent = job.position;
        document.getElementById('modal-period').textContent = `${job.start_date} ~ ${job.end_date}`;
        
        const descContainer = document.getElementById('modal-description');
        descContainer.innerHTML = '';

        if (job.summary_data && Object.keys(job.summary_data).length > 0) {
            const s = job.summary_data;
            let html = '';
            
            if (s.role_summary) html += `<h4>📋 Role Summary</h4><p>${s.role_summary}</p>`;
            
            if (s.key_requirements && s.key_requirements.length > 0) {
                html += `<h4>✅ Key Requirements</h4><ul>`;
                s.key_requirements.forEach(r => html += `<li>${r}</li>`);
                html += `</ul>`;
            }
            
            if (s.preferences && s.preferences.length > 0) {
                html += `<h4>⭐ Preferences</h4><ul>`;
                s.preferences.forEach(p => html += `<li>${p}</li>`);
                html += `</ul>`;
            }
            
            if (s.summary) html += `<h4>💡 Summary</h4><p>${s.summary}</p>`;
            
            descContainer.innerHTML = html || job.description;
        } else {
            descContainer.textContent = job.description || 'No description available.';
        }
        
        let skillsText = '';
        if (job.skills && job.skills.length > 0) {
            skillsText = job.skills.join(', ');
        } else {
            skillsText = 'Not specified';
        }
        document.getElementById('modal-skills').textContent = skillsText;
        
        const linkElem = document.getElementById('modal-link');
        if(job.application_url) {
            linkElem.href = job.application_url;
            linkElem.style.display = 'inline-block';
        } else {
            linkElem.style.display = 'none';
        }

        document.getElementById('job-modal').style.display = 'block';
    }
}
