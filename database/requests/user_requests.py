from database.repository import BaseRepository
from database.models import User
from sqlalchemy import select, update, delete, and_, func, desc
from typing import Optional, List, Tuple, Dict
from datetime import datetime
import time




class UserRequests(BaseRepository):
    async def create_user(self, tg_id: int) -> Optional[User]:
        async with self.begin():
            user = await getUser(tg_id)
            if not user:
                unix_time = int(time.time())
                user = User(tg_id = tg_id, start_date = unix_time)
                self.session.add(user)
            return user
    


    async def get_user(self, tg_id: int) -> Optional[User]:
        async with self.begin():
            user = await self.session.scalar(
                select(User).where(User.tg_id == tg_id)
            )
            return user


    
    async def get_cigarette_count(self, tg_id: int) -> Optional[User]:
        async with self.begin():
            user = await self.session.scalar(
                select(User).where(User.tg_id == tg_id)
            )
            return user.cigarette_count



    async def get_cigarette_price(self, tg_id: int) -> Optional[User]:
        async with self.begin():
            user = await self.session.scalar(
                select(User).where(User.tg_id == tg_id)
            )
            return user.cigarette_price



    async def set_cigarette_count(self, tg_id: int, count: int) -> Optional[User]:
        async with self.begin():
            user = await self.session.scalar(
                select(User).where(User.tg_id == tg_id)
            )
            user.cigarette_count = count
            return user
        


    async def set_cigarette_price(self, tg_id: int, price: int) -> Optional[User]:
        async with self.begin():
            user = await self.session.scalar(
                select(User).where(User.tg_id == tg_id)
            )
            user.cigarette_price = price
            return user

################################################
"""Функции-обертки для обратной совместимости"""
################################################


async def createUser(tg_id: int) -> Optional[User]:
    async with UserRequests() as repo:
        return await repo.create_user(tg_id)



async def getUser(tg_id: int) -> Optional[User]:
    async with UserRequests() as repo:
        return await repo.get_user(tg_id)



async def getCigaretteCount(tg_id: int) -> Optional[User]:
    async with UserRequests() as repo:
        return await repo.get_cigarette_count(tg_id)



async def getCigarettePrice(tg_id: int) -> Optional[User]:
    async with UserRequests() as repo:
        return await repo.get_cigarette_price(tg_id)



async def setCigaretteCount(tg_id: int, count: int) -> Optional[User]:
    async with UserRequests() as repo:
        return await repo.set_cigarette_count(tg_id, count)



async def setCigarettePrice(tg_id: int, price: int) -> Optional[User]:
    async with UserRequests() as repo:
        return await repo.set_cigarette_price(tg_id, price)
