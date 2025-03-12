from database.repository import BaseRepository
from database.models import User
from sqlalchemy import select, update, delete, and_, func, desc
from typing import Optional, List, Tuple, Dict
from datetime import datetime
import time