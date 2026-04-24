# Masterblog-API

A simple educational REST API for managing blog posts built with Flask.

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: JavaScript, HTML, CSS
- **Features**: CORS, rate limiting, Swagger documentation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/84edu/Masterblog-API.git
cd Masterblog-API
```

2. Install dependencies:
```bash
pip install flask flask-cors flask-limiter flask-swagger-ui
```

3. Run the backend:
```bash
python backend/backend_app.py
```

The API will be available at `http://localhost:5002`

## API Endpoints

### Get All Posts
```
GET /api/v1/posts?page=1&limit=10&sort=title&direction=asc
```

### Create a Post
```
POST /api/v1/posts
Content-Type: application/json

{
  "title": "Post Title",
  "content": "Post content here"
}
```

### Update a Post
```
PUT /api/v1/posts/{id}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

### Delete a Post
```
DELETE /api/v1/posts/{id}
```

### Search Posts
```
GET /api/v1/posts/search?title=keyword
GET /api/v1/posts/search?content=keyword
```

## Rate Limiting

- Global: 200 requests per day, 50 per hour
- GET posts: 5 requests per minute

## Documentation

Access Swagger UI at: `http://localhost:5002/api/v1/docs`

## License

Educational purposes only.
