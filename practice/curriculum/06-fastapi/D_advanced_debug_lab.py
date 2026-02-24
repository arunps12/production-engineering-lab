"""
Section 6 — FastAPI: Advanced Debug Lab
Guide: docs/curriculum/06-fastapi-professional.md

Exercise 4.D.1 — async def Blocks the Event Loop
Exercise 4.D.3 — Dependency Not Cleaning Up
Exercise 4.D.4 — Middleware Order Matters
"""

# Exercise 4.D.1 — async def Blocks the Event Loop
# BUG: CPU-bound work in async handler blocks everything
# import time
# from fastapi import FastAPI
# app = FastAPI()
#
# @app.get("/slow")
# async def slow_endpoint():
#     time.sleep(5)  # BUG: Blocks the event loop!
#     return {"status": "done"}
#
# TODO: Fix by using def (not async def) or run_in_executor


# Exercise 4.D.3 — Dependency Not Cleaning Up
# BUG: Database connection not closed on error
# async def get_db():
#     db = connect()
#     return db  # BUG: No cleanup!
#
# TODO: Fix with yield and try/finally
# async def get_db():
#     db = connect()
#     try:
#         yield db
#     finally:
#         db.close()


# Exercise 4.D.4 — Middleware Order Matters
# TODO: Understand that middleware executes in reverse order of registration
