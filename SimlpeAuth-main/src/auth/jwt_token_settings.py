from authx import AuthX, AuthXConfig

config = AuthXConfig(
    JWT_SECRET_KEY='',
    JWT_TOKEN_LOCATION=['cookies']
)

security = AuthX(config=config)

