async def save_investition(target, sources, session):
    session.add(target)
    session.add_all(sources)
    await session.commit()
    await session.refresh(target)
    return target
