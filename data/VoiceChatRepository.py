from dataclasses import dataclass
from typing import List

import discord
from datetime import datetime, UTC, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, case
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# --- SQLAlchemy setup ---
Base = declarative_base()

class VoiceSession(Base):
    __tablename__ = "VoiceSessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    guild_id = Column(String, nullable=False)
    channel_name = Column(String, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    left_at = Column(DateTime)

@dataclass
class TopVCUser:
    user_id: str
    username: str
    total_seconds: float

class VoiceSessionRepository:
    """Manages persistence of active and completed voice sessions."""

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def start_session(self, member: discord.Member, channel_name: str) -> None:
        """Create a new session when a user joins a channel."""
        with self.SessionLocal() as session:
            new_session = VoiceSession(
                user_id=str(member.id),
                username=member.name,
                guild_id=str(member.guild.id),
                channel_name=channel_name,
                joined_at=datetime.now(UTC),
            )
            session.add(new_session)
            session.commit()

    def end_session(self, member: discord.Member, channel_name: str) -> None:
        """Mark an existing session as ended when a user leaves or switches."""
        with self.SessionLocal() as session:
            active = (
                session.query(VoiceSession)
                .filter(
                    VoiceSession.user_id == str(member.id),
                    VoiceSession.guild_id == str(member.guild.id),
                    VoiceSession.channel_name == channel_name,
                    VoiceSession.left_at.is_(None),
                )
                .order_by(VoiceSession.joined_at.desc())
                .first()
            )
            if active:
                active.left_at = datetime.now(UTC)
                session.commit()

    def get_vc_time_elapsed(self, member_id: str, since: datetime) -> int:
        """Return the total time spent in voice channels since a given datetime."""
        with self.SessionLocal() as session:
            total_seconds = session.query(
                func.sum(
                    func.extract(
                        'epoch',
                        case(
                            (VoiceSession.left_at != None, VoiceSession.left_at),
                            else_=datetime.utcnow()
                        ) - VoiceSession.joined_at
                    )
                )
            ).filter(
                VoiceSession.user_id == member_id,
                VoiceSession.joined_at >= since
            ).scalar()

        return int(total_seconds or 0)

    def get_top_vc_chatters(self, top_n: int, days: int) -> List[TopVCUser]:
        """
        Returns a list of TopVCUser instances for the top `n` users by VC time in the last `days`.
        """
        since = datetime.utcnow() - timedelta(days=days)

        with self.SessionLocal() as session:
            results = session.query(
                VoiceSession.user_id,
                VoiceSession.username,
                func.sum(
                    func.extract(
                        'epoch',
                        case(
                            (VoiceSession.left_at != None, VoiceSession.left_at),
                            else_=datetime.utcnow()
                        ) - VoiceSession.joined_at
                    )
                ).label("total_seconds")
            ).filter(
                VoiceSession.joined_at >= since
            ).group_by(
                VoiceSession.user_id,
                VoiceSession.username
            ).order_by(
                func.sum(
                    func.extract(
                        'epoch',
                        case(
                            (VoiceSession.left_at != None, VoiceSession.left_at),
                            else_=datetime.utcnow()
                        ) - VoiceSession.joined_at
                    )
                ).desc()
            ).limit(top_n).all()

        return [
            TopVCUser(user_id=user_id, username=username, total_seconds=total_seconds or 0)
            for user_id, username, total_seconds in results
        ]