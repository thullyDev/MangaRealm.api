<h1 align="center">
MangaRealm API
</h1>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href="#"><img src="https://img.shields.io/badge/fastapi-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI Badge"/></a>
  <a href="#"><img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL Badge"/></a>
  <a href="#"><img src="https://img.shields.io/badge/redis-%23DC382D.svg?style=for-the-badge&logo=redis&logoColor=white" alt="Redis Badge"/></a>
</p>

<p align="center">
  <a href="#" target="_blank">
    <img src="https://thullydev.github.io/thullyDevStatics/images/mangarealm-logo.png" alt="Logo" width="200"/>
  </a>
</p>

## What is MangaRealm API?

Welcome to the **MangaRealm API** - the backend powerhouse driving the MangaRealm experience! This API is designed to handle user profiles, manga lists, and various user-related operations for the MangaRealm platform.

Built with **FastAPI**, our API provides fast and efficient endpoints for managing user data, manga lists, and profile information. It integrates with **PostgreSQL** for data persistence and **Redis** for caching, ensuring optimal performance and responsiveness.

## Features

- User profile management
- Manga list operations (add, remove, check)
- User information updates
- Profile image upload and management
- Authentication token generation and validation
- Pagination support for manga lists

## API Endpoints

- `/api/profile_details/`: Get user profile details and manga list
- `/api/add_to_list`: Add a manga to user's list
- `/api/remove_from_list`: Remove a manga from user's list
- `/api/change_user_info`: Update user information
- `/api/upload_user_profile_image`: Upload and update user's profile image
- `/api/is_in_list/`: Check if a manga is in user's list


This API serves as the backbone for the MangaRealm platform, handling crucial backend operations and ensuring a smooth, responsive experience for manga enthusiasts.