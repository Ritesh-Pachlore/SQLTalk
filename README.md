# SQL Talk - Natural Language to SQL Query Converter

SQL Talk is an AI-powered application that converts natural language questions into SQL queries and executes them against a SQLite database. It uses the Google Gemini API to understand natural language and generate appropriate SQL queries.

## Features

- Convert natural language questions to SQL queries
- Execute SQL queries against a SQLite database
- User-friendly web interface built with Streamlit
- Support for student database queries (expandable to other databases)
- Auto-retry mechanism for API rate limits
- Error handling and user feedback

## Demo

[Add screenshots or GIF here showing the application in action]

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/SQLTalk.git
cd SQLTalk
```

2. Create a virtual environment and activate it:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Google Gemini API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

1. Start the Streamlit application:

```bash
streamlit run sql.py
```

2. Open your web browser and go to `http://localhost:8501`

3. Enter your question in natural language (e.g., "Show me all students in Data Science class")

4. View the SQL query results displayed on the page

## Database Schema

The current implementation uses a SQLite database with the following schema:

```sql
CREATE TABLE STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
```

## Example Queries

- "How many students are there in total?"
- "Show all students in Data Science class"
- "List students with marks above 90"
- "What is the average marks in each class?"

## Configuration

You can customize the application behavior through the `.streamlit/config.toml` file:

- Theme settings
- Server settings
- Custom color schemes

## Deployment

This application can be deployed on Streamlit Cloud:

1. Push your code to GitHub
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy from your GitHub repository
4. Add your environment variables in Streamlit Cloud settings

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Google Gemini API for natural language processing
- Streamlit for the web interface
- SQLite for database management

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)
Project Link: [https://github.com/yourusername/SQLTalk](https://github.com/yourusername/SQLTalk)
