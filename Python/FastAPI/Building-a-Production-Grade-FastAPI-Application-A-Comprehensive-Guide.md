## https://www.youtube.com/watch?v=SR5NYCdzKkc

Here is a comprehensive educational guide based on the provided transcription. This guide covers every concept, theory, and code implementation discussed in the video, designed to take you from API theory to building a production-grade backend using FastAPI, SQLAlchemy, and ImageKit.

---

# Building a Production-Grade FastAPI Application: A Comprehensive Guide

In this guide, we will build a full-stack, early-Instagram-style photo and video sharing application. While we will briefly look at a Streamlit frontend, our primary focus will be on building a robust backend using **FastAPI**. 

We will cover everything from the absolute basics of API development to advanced concepts such as database connections, handling image/video uploads, and setting up secure user authentication (JWT).

*Prerequisites: Basic to intermediate knowledge of Python is assumed.*

---

## Part 1: Web App and API Theory

Before writing code, it is critical to understand how web applications and APIs communicate.

### What is an API?
**API** stands for **Application Programming Interface**. In the context of web development, a backend API (like the one we are building with FastAPI) runs on a server. It acts as a secure layer that facilitates the access and control of your application's data (e.g., user accounts, image posts). 

### URLs and Endpoints
When accessing an API, you interact with URLs. A typical URL consists of several parts:
1. **Domain:** The website space (e.g., `techwithtim.net`, `api.com`).
2. **Path (or Endpoint):** The specific route or resource being accessed. For example, in `api.com/posts/123`, `/posts/123` is the path.
3. **Query Parameters:** Extra information used to filter data. They appear after a question mark `?` and are separated by ampersands `&`. For example: `?video=123&utm_source=youtube`.

### The Client-Server Relationship (Request and Response)
1. **The Client (Front End):** The visual interface the user interacts with (e.g., a website or mobile app). 
2. **The Server (Back End/API):** The secure location where data operations happen.

When a user performs an action on the front end (like deleting a post), the Client sends a **Request** to the Server. The Server processes it and sends back a **Response**.

#### Structure of a Request
*   **Method (Type):** Indicates the action the client wants to perform.
    *   `GET`: Retrieve data.
    *   `POST`: Create new data.
    *   `PUT` / `PATCH`: Update existing data.
    *   `DELETE`: Remove data.
*   **Path:** The endpoint being targeted (e.g., `/api/posts/123`).
*   **Body (Optional):** Additional data sent with the request (e.g., the image file, or the text for a new caption).
*   **Headers:** Metadata, typically including security and authentication tokens.

#### Structure of a Response
*   **Status Code:** A numerical code indicating the result of the request.
    *   `200`: OK (Success).
    *   `201`: Created (Success).
    *   `204`: No Content (Successfully updated/deleted).
    *   `404`: Not Found.
    *   `500`: Internal Server Error.
*   **Body:** The data returned to the client (often in JSON format).
*   **Headers:** Metadata about the response, such as the data format (`application/json`).

### Authentication Primer (JWT)
To secure our API, we use **JWT (JSON Web Tokens)**. 
1. A user sends their username and password to an authentication endpoint.
2. The server verifies the credentials and returns a unique, encrypted string called a JWT.
3. The client stores this JWT and includes it in the **Headers** of every subsequent request.
4. The server reads the JWT, identifies the user, and authorizes the action.

---

## Part 2: Project Setup and Dependencies

For this project, we recommend using the **PyCharm** IDE. To manage our packages, we will use **uv** (a modern Python package manager), though `pip` works identically.

1. Create an empty folder (e.g., `fastapi-tutorial`) and open it in your IDE.
2. Open your terminal and initialize the project:
   ```bash
   uv init .
   ```
3. Install the required dependencies:
   ```bash
   uv add fastapi
   uv add python-dotenv
   uv add 'fastapi-users[sqlalchemy]'
   uv add imagekitio
   uv add 'uvicorn[standard]'
   uv add aiosqlite
   ```

### Setting Up Environment Variables (ImageKit)
Handling file uploads manually is notoriously difficult. We will use a free service called **ImageKit** to host our images and videos.
1. Create a free account at imagekit.io.
2. Navigate to Developer Options to find your API keys.
3. In your project root, create a file named `.env` and store your credentials securely:

```env
IMAGEKIT_PRIVATE_KEY=your_private_key_here
IMAGEKIT_PUBLIC_KEY=your_public_key_here
IMAGEKIT_URL=your_url_endpoint_here
```
*(Note: Never share your `.env` file or commit it to GitHub).*

---

## Part 3: FastAPI Basics

Let's create the scaffolding for our application. Create a folder named `app` and inside it, a file named `app.py`. We will also configure a `main.py` file in the root directory to run the server.

### Creating a Basic Endpoint (`app/app.py`)
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello-world")
def hello_world():
    return {"message": "Hello World"}
```
*   `app = FastAPI()` initializes our application.
*   `@app.get(...)` is a Python decorator specifying that a `GET` request to `/hello-world` will trigger the function beneath it.
*   We return a Python dictionary. FastAPI automatically converts this into JSON (JavaScript Object Notation), which is the standard data format for web APIs.

### Running the Server (`main.py`)
To run the app, we use **Uvicorn**, an asynchronous web server.

```python
import uvicorn

if __name__ == "__main__":
    # "app.app:app" refers to the folder "app", the file "app.py", and the variable "app"
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True)
```
*Run the file using `python main.py` or `uv run main.py`.*
*   `host="127.0.0.1"` runs the server locally.
*   `reload=True` ensures the server automatically restarts whenever you save code changes.

### The Auto-Generated Documentation (`/docs`)
FastAPI's best feature is its automatic interactive documentation. If you navigate to `http://127.0.0.1:8000/docs` in your browser, you will see a Swagger UI page. Here, you can visually test your endpoints by clicking "Try it out" and "Execute" without needing a custom front end.

---

## Part 4: Routing, Parameters, and Data Validation

Before connecting a database, let's learn how to handle data dynamically using temporary in-memory dictionaries. 

### Path Parameters and HTTP Exceptions
Let's create an endpoint to retrieve a specific post by its ID. We define a path parameter by wrapping a variable in curly braces `{}`.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

text_posts = {
    1: {"title": "New Post", "content": "Cool test post"},
    2: {"title": "Second Post", "content": "Another post"}
}

@app.get("/post/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts[id]
```
*   `id: int`: This is a Python type hint. FastAPI uses this to automatically validate incoming data. If a user requests `/post/abc`, FastAPI will automatically reject it because `abc` is not an integer.

### Query Parameters
Query parameters are optional variables appended to the URL. If a function parameter is not part of the URL path, FastAPI assumes it is a query parameter.

```python
@app.get("/posts")
def get_all_posts(limit: int = None):
    posts_list = list(text_posts.values())
    if limit:
        return posts_list[:limit]
    return posts_list
```
*Testing this in the `/docs` allows you to pass a limit (e.g., `3`) to see only the first 3 posts.*

### Request Bodies and Pydantic Schemas
To create a post, the user must send data in the **Request Body**. In FastAPI, we define the expected structure of this data using a library called Pydantic. 

Create a file `app/schemas.py`:
```python
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    title: str
    content: str
```

Now, update `app.py` to use these schemas:
```python
from app.schemas import PostCreate, PostResponse

@app.post("/post", response_model=PostResponse)
def create_post(post: PostCreate):
    new_id = max(text_posts.keys()) + 1 if text_posts else 1
    new_post = {
        "title": post.title,
        "content": post.content
    }
    text_posts[new_id] = new_post
    return new_post
```
*   **Validation:** Because `post` is typed as `PostCreate`, FastAPI guarantees that the incoming request has a `title` and `content` that are strings.
*   **Response Model:** Adding `response_model=PostResponse` in the decorator ensures that the outbound data strictly matches our schema. This adds a layer of security and improves the `/docs` UI.

---

## Part 5: Database Setup (SQLAlchemy)

In-memory dictionaries reset when the server restarts. To persist data, we need a database. We will use **SQLite** combined with **SQLAlchemy**, an Object Relational Mapper (ORM) that allows us to write Python code instead of raw SQL queries.

Create `app/db.py`:

```python
import uuid
from datetime import datetime
from collections.abc import AsyncGenerator
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship

# Database connection URL (local SQLite file)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

# Define our Database Model
class Post(Base):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Engine and Session configuration
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Function to create tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency to get the database session in our routes
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
```

### Initializing the Database on Startup
To ensure tables are created when our app boots up, we use an asynchronous context manager in `app/app.py`:

```python
from contextlib import asynccontextmanager
from app.db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
```
Upon running the app, a `test.db` file will appear in your project folder.

---

## Part 6: File Uploads and ImageKit Integration

Now we implement real logic for our photo/video app, replacing our dummy endpoints.

### Setting up ImageKit (`app/images.py`)
Create a file to initialize ImageKit using our environment variables:

```python
import os
from dotenv import load_dotenv
from imagekitio import ImageKit

load_dotenv()

imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL")
)
```

### The Upload Endpoint (`app/app.py`)
To accept files, we use `UploadFile` and `Form` from FastAPI. Because we want to upload securely from our backend, we will save the incoming file to a temporary file, push it to ImageKit, and then delete the temporary file.

```python
import tempfile
import shutil
import os
from fastapi import File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from app.db import get_async_session, Post
from app.images import imagekit

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...), 
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session) # Dependency Injection
):
    temp_file_path = None
    try:
        # 1. Create a temporary file with the correct extension
        ext = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # 2. Upload to ImageKit
        options = UploadFileRequestOptions(
            use_unique_file_name=True,
            tags=["backend_upload"]
        )
        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.upload_file(
                file=f,
                file_name=file.filename,
                options=options
            )

        if upload_result.response_metadata.http_status_code == 200:
            # 3. Save to Database
            file_type = "video" if file.content_type.startswith("video/") else "image"
            
            new_post = Post(
                caption=caption,
                url=upload_result.url,
                file_type=file_type,
                file_name=upload_result.name
            )
            session.add(new_post)
            await session.commit()
            await session.refresh(new_post) # Hydrates the object with generated ID and Date
            
            return new_post
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 4. Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()
```
*   **Dependency Injection (`Depends`):** FastAPI automatically calls `get_async_session`, providing us with the `session` variable to interact with the database inside the route.

### Retrieving and Deleting Posts
We need routes to fetch our feed and delete specific posts.

```python
from sqlalchemy import select
import uuid

@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    # Query posts, ordered by newest first
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]
    
    post_data = []
    for post in posts:
        post_data.append({
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
        })
    return post_data

@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
            
        await session.delete(post)
        await session.commit()
        return {"success": True, "message": "Post deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Note on ImageKit Transformations
A major benefit of ImageKit is the ability to transform images dynamically via the URL. By modifying the URL parameters, you can alter the media on the fly. 
For example, adding `tr=w-500,h-500` resizes the image. Adding `tr=e-contrast` adjusts contrast, and adding `/ik-thumbnail.jpg` to a video URL fetches its thumbnail.

---

## Part 7: Authentication with FastAPI Users

Currently, anyone can upload or delete a post. We must secure our application by implementing user authentication. We will use the `fastapi-users` library to abstract the heavy lifting of JWT token management.

### 1. Database Updates (One-To-Many Relationships)
First, update `app/db.py` to include a User model and establish a relationship between Users and Posts.

```python
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

# Add the User Model
class User(SQLAlchemyBaseUserTableUUID, Base):
    # One User has many Posts
    posts = relationship("Post", back_populates="user")

# Update the Post Model (Add foreign key and relationship)
class Post(Base):
    __tablename__ = "post"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # NEW: Link post to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="posts")

# Add a database dependency for Users
from fastapi import Depends

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
```

### 2. User Schemas
Create Pydantic models for users in `app/schemas.py`:

```python
import uuid
from fastapi_users import schemas

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass
```

### 3. Configuring FastAPI Users Backend (`app/users.py`)
Create `app/users.py` to configure JWT strategies and the user manager.

```python
import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from app.db import User, get_user_db

SECRET = "super_secret_string_do_not_share" # Used to sign JWTs securely

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    
    # You can hook into lifecycle events:
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.email} has registered.")

async def get_user_manager(user_db = Depends(get_user_db)):
    yield UserManager(user_db)

# Configure JWT Authentication
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600) # Valid for 1 hour

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
```

### 4. Injecting Auth Routes into FastAPI (`app/app.py`)
Now, include the pre-built authentication routes in your main application:

```python
from app.users import auth_backend, fastapi_users, current_active_user
from app.schemas import UserRead, UserCreate

# Login/Logout routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

# Registration routes
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
```
*If you check `/docs` now, you will see new endpoints for `/auth/jwt/login` and `/auth/register`.*

### 5. Protecting Our Endpoints
Finally, update the post and upload routes to require a signed-in user, and enforce ownership rules.

**Update `/upload`:**
```python
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...), 
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user) # ENFORCES LOGIN
):
    # ... Image upload logic remains the same ...
    
    # Save user_id to post
    new_post = Post(
        caption=caption,
        url=upload_result.url,
        file_type=file_type,
        file_name=upload_result.name,
        user_id=user.id # Bind post to user
    )
    # ...
```

**Update `/posts/{post_id}` (Delete route):**
```python
@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    # ... Retrieve post logic ...
    
    # Authorization Check
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
        
    # ... Delete logic ...
```

**Update `/feed`:**
```python
from app.db import User

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    # Get all posts
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]
    
    # Helper to get user emails
    user_result = await session.execute(select(User))
    users_list = [row[0] for row in user_result.all()]
    user_dict = {u.id: u.email for u in users_list}
    
    post_data = []
    for post in posts:
        post_data.append({
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "created_at": post.created_at.isoformat(),
            "user_id": str(post.user_id),
            "email": user_dict.get(post.user_id, "Unknown"),
            "is_owner": post.user_id == user.id # True if the current user made the post
        })
    return post_data
```

---

## Part 8: Frontend (Streamlit) Overview

While the video focuses on the backend, it utilizes a **Streamlit** front end to visually interact with the API. 
*(To run this, install streamlit via `uv add streamlit` and run `uv run streamlit run frontend.py`)*

The frontend logic revolves around sending HTTP requests to the endpoints we just built:
1. **Login:** Takes a username and password, sends it to `/auth/jwt/login`, and receives the JWT.
2. **Session State:** Streamlit stores the JWT in its internal session memory.
3. **Authorized Requests:** For actions like Uploading or loading the Feed, Streamlit attaches the JWT in the Request Header (`{"Authorization": f"Bearer {token}"}`).
4. **Rendering Images/Videos:** The frontend takes the `url` returned in the feed. Using ImageKit's dynamic capabilities, the front end can append transformation strings to the URL to layer text (captions) directly onto images, crop videos, or reduce file quality on the fly before rendering them on the screen.

---

### Conclusion

By following this guide, you have built a production-ready Backend API. You implemented **FastAPI** routing, data validation using **Pydantic**, asynchronous database mapping with **SQLAlchemy**, external cloud asset management with **ImageKit**, and a secure JSON Web Token authentication system using **FastAPI Users**.
