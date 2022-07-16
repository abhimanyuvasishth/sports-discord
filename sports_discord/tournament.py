from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.orm import registry

from sports_discord.google_sheet import get_sheet

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Tournament:
    __tablename__ = "tournament"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    series_id: str = field(metadata={"sa": Column(String)})
    channel_id: str = field(metadata={"sa": Column(String, unique=True)})
    doc_name: str = field(metadata={"sa": Column(String)})
    points_sheet_name: str = field(default='Points Worksheet', metadata={"sa": Column(String)})
    bidding_sheet_name: str = field(default='Bidding Page', metadata={"sa": Column(String)})
    team_points_sheet_name: str = field(default='Team Points', metadata={"sa": Column(String)})
    sheet_url: str = field(init=False, metadata={"sa": Column(String)})
    active: bool = field(default=False, metadata={"sa": Column(Boolean)})
    creation_timestamp: str = field(
        default_factory=datetime.utcnow, metadata={"sa": Column(TIMESTAMP)}
    )

    def __post_init__(self):
        sheet = get_sheet(doc_name=self.doc_name, sheet_name=self.team_points_sheet_name)
        self.sheet_url = sheet.spreadsheet.url
