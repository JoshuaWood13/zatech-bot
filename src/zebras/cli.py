from __future__ import annotations

import asyncio
import logging
import click
import uvicorn

from .config import load_settings
from .logging import setup_logging
from .router import Router
from .plugin.registry import Registry
from .slack.socket import SocketApp
from .http.app import create_app
from .storage.kv import create_redis
from .worker.queue import start_worker
from .storage.datastore import create_engine
from .app_context import AppContext, set_context
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
import os


def _load_plugins(reg: Registry) -> None:
    # For now, import built-in logging plugin. External discovery can be added later.
    from .plugins.logging import register as logging_register
    from .plugins.rules import register as rules_register

    logging_register(reg)
    rules_register(reg)


@click.group()
def cli() -> None:
    """ZEBRAS CLI."""


@cli.command()
def socket() -> None:
    """Run Socket Mode app."""
    s = load_settings()
    setup_logging(s.log_level)
    if not s.slack_app_token:
        raise SystemExit("SLACK_APP_TOKEN required for socket mode")
    router = Router()
    reg = Registry()
    _load_plugins(reg)
    # Bind registry handlers to router
    for etype, handlers in reg.event_handlers.items():
        for h in handlers:
            router.on(etype, h)

    # Initialize context (DB + Redis)
    engine = create_engine(s.database_url)
    r = create_redis(s.redis_url)
    set_context(AppContext(engine=engine, redis=r))

    app = SocketApp(s.slack_bot_token, s.slack_app_token, router, reg)
    asyncio.run(app.run())


@cli.command()
@click.option("--host", default=None)
@click.option("--port", default=None, type=int)
def http(host: str | None, port: int | None) -> None:
    """Run HTTP Events API server."""
    s = load_settings()
    setup_logging(s.log_level)
    router = Router()
    reg = Registry()
    _load_plugins(reg)
    for etype, handlers in reg.event_handlers.items():
        for h in handlers:
            router.on(etype, h)

    # Initialize context (DB + Redis)
    engine = create_engine(s.database_url)
    r = create_redis(s.redis_url)
    set_context(AppContext(engine=engine, redis=r))

    app = create_app(router, s.slack_signing_secret, reg)
    uvicorn.run(app, host=host or s.http_host, port=port or s.http_port)


@cli.command()
@click.option("--queue", default="zebras")
def worker(queue: str) -> None:
    """Run background job worker (RQ)."""
    s = load_settings()
    setup_logging(s.log_level)
    r = create_redis(s.redis_url)
    start_worker(r, queue)


def _alembic_config() -> AlembicConfig:
    cfg = AlembicConfig("alembic.ini")
    # Pass DATABASE_URL from env to alembic
    if "DATABASE_URL" in os.environ:
        cfg.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
    return cfg


@cli.group()
def db() -> None:
    """Database migration commands."""


@db.command("upgrade")
@click.argument("revision", default="head")
def db_upgrade(revision: str) -> None:
    setup_logging("INFO")
    cfg = _alembic_config()
    alembic_command.upgrade(cfg, revision)


@db.command("downgrade")
@click.argument("revision", default="base")
def db_downgrade(revision: str) -> None:
    setup_logging("INFO")
    cfg = _alembic_config()
    alembic_command.downgrade(cfg, revision)


def main() -> None:
    cli(standalone_mode=True)
