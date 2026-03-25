# REST API Endpoint Corrections

**Data:** 2024-07-20

---

**User:**

Using best practices while creating REST API, correct the following endpoints
GET /comments/{videoId}
GET  /comments/sentiment/ {videoId}
GET /comments/offended/
{videoId}
DELETE /comments/{videoId}/
{commentIds}

---

**Assistant:**

When designing RESTful APIs, it's important to follow best practices to ensure the API is intuitive, easy to use, and maintainable. This involves using clear, logical, and consistent naming conventions, as well as ensuring that the endpoints are well-structured and adhere to standard HTTP methods.

Here are the corrected endpoints:

1. **Get comments for a specific video:**
   - Original: `GET /comments/{videoId}`
   - Corrected: `GET /videos/{videoId}/comments`
     - **Reason:** It's more intuitive to nest comments under the relevant resource (in this case, videos), indicating a clear parent-child relationship.

2. **Get sentiment of comments for a specific video:**
   - Original: `GET /comments/sentiment/{videoId}`
   - Corrected: `GET /videos/{videoId}/comments/sentiment`
     - **Reason:** Similarly, nesting sentiment under the specific video comments keeps the API consistent and makes it clear that the sentiment relates to the comments of that specific video.

3. **Get offended comments for a specific video:**
   - Original: `GET /comments/offended/{videoId}`
   - Corrected: `GET /videos/{videoId}/comments/offended`
     - **Reason:** Following the same logic, nesting offended comments under the specific video provides clarity and maintains consistency.

4. **Delete specific comments for a specific video:**
   - Original: `DELETE /comments/{videoId}/{commentIds}`
   - Corrected: `DELETE /videos/{videoId}/comments/{commentId}`
     - **Reason:** To follow REST principles, it's better to delete one comment at a time with a specific endpoint for that comment. If multiple comments need to be deleted, the client can make multiple requests or, if batch operations are supported, use a different endpoint such as `DELETE /videos/{videoId}/comments` with a request body containing the list of `commentIds`.

   - Alternative for batch delete:
     - `DELETE /videos/{videoId}/comments`
     - **Reason:** Accepting a list of `commentIds` in the request body for batch deletions. This approach keeps the URL clean and allows batch operations while adhering to REST principles.

### Summary of Corrected Endpoints

1. Get comments for a specific video:
   ```
   GET /videos/{videoId}/comments
   ```

2. Get sentiment of comments for a specific video:
   ```
   GET /videos/{videoId}/comments/sentiment
   ```

3. Get offended comments for a specific video:
   ```
   GET /videos/{videoId}/comments/offended
   ```

4. Delete a specific comment for a specific video:
   ```
   DELETE /videos/{videoId}/comments/{commentId}
   ```

   - For batch deletion:
     ```
     DELETE /videos/{videoId}/comments
     ```
     - Request body: `{ "commentIds": ["id1", "id2", ...] }`

These changes ensure that the API endpoints are intuitive, consistent, and adhere to RESTful principles.

---

**User:**

in GET /videos/{videoId}/comments/offended shpuld videos be in plural? or video?

---

**Assistant:**

In RESTful API design, using plural nouns for resource names is generally considered a best practice because it helps maintain consistency and clarity, especially when dealing with collections of resources. Therefore, `videos` should be in plural form.

### Corrected Endpoint:

Get offended comments for a specific video:
```
GET /videos/{videoId}/comments/offended
```

### Reason:
- Using `videos` (plural) follows the convention and indicates that the endpoint is part of a collection of videos, making it more intuitive and consistent with other similar endpoints.

In summary, using plural nouns for resource names helps create a consistent and understandable API structure. Therefore, keeping `videos` in plural form is the correct approach.

---

**User:**

Suggest the enpoint name for operation of giving shadow ban for an author of a comment

---

**Assistant:**

When designing an endpoint for shadow banning an author of a comment, it's important to clearly convey the action being performed. Shadow banning is an operation that affects a user (the author of a comment) based on their behavior or content they've posted. Therefore, the endpoint should reflect this action and the targeted user.

Here’s a suggested endpoint name for this operation:

### Suggested Endpoint:

Shadow ban the author of a comment:
```
POST /comments/{commentId}/author/shadow-ban
```

### Reasoning:
- **POST:** Using the `POST` method indicates that this operation will create or trigger an action (in this case, shadow banning).
- **/comments/{commentId}/author:** This part of the path specifies that the action is related to the author of a specific comment.
- **/shadow-ban:** This clearly describes the action being performed on the author.

### Example Usage:
```
POST /comments/12345/author/shadow-ban
```

In this example, `12345` is the `commentId`, and the action shadow bans the author of that specific comment. This naming convention keeps the endpoint intuitive and clear in terms of its purpose and the action being performed.