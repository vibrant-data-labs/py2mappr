from typing import Any, Callable, Dict, List
import pathlib as pl
from .._project_manager import get_project
from .._builder import build_map

__directory: pl.Path = None


def set_player_directory(directory: pl.Path):
    global __directory
    __directory = directory


def local(web_dir: pl.Path = None, PORT=8080) -> Callable[[Callable], None]:
    """
    Decorator to run a local player.
    """
    from .local_worker import local_worker

    def get_web_dir(data: Dict[str, Any]) -> pl.Path:
        if web_dir is None:
            return data.get("web_dir")
        return web_dir

    return lambda data: local_worker(web_dir=get_web_dir(data), PORT=PORT)


def s3(
    bucket_name: str, web_dir: pl.Path = None
) -> Callable[[Callable], None]:
    """
    Decorator to upload local player files to the s3. Requires [aws] setting of
    config.ini to be set.
    """
    from .s3_worker import s3_worker

    def get_web_dir(data: Dict[str, Any]) -> pl.Path:
        if web_dir is None:
            return data.get("web_dir")
        return web_dir

    return lambda data: s3_worker(
        path=get_web_dir(data), bucket_name=bucket_name
    )


def ec2(url: str, region: str = None) -> Callable[[Callable], None]:
    """
    Decorator to set up the ec2 instance. Requires [deploy_agent] setting of
    config.ini to be set.
    """
    from .ec2_worker import ec2_worker

    def get_region(data: Dict[str, Any]) -> str:
        if region is None:
            return data.get("region")
        return region

    return lambda data: ec2_worker(
        bucket=data.get("bucket"), url=url, region=get_region(data)
    )


def cloudfront(
    url: str, bucket_name: str = None
) -> Callable[[Callable], None]:
    """
    Decorator to set up the cloudfront distribution. Requires [aws] setting of
    config.ini to be set.
    """
    from .cloudfront_worker import cloudfront_worker

    def get_bucket_name(data: Dict[str, Any]) -> str:
        if bucket_name is None:
            return data.get("bucket")
        return bucket_name

    return lambda data: cloudfront_worker(
        bucket=get_bucket_name(data), url=url
    )


def cloudflare(url: str, cdn_url: str = None) -> Callable[[Callable], None]:
    """
    Decorator to set up the DNS for the player url in the cloudflare. Requires
    [cloudflare] setting of config.ini to be set.
    """
    from .cloudflare_worker import cloudflare_worker

    def get_cdn_url(data: Dict[str, Any]) -> str:
        if cdn_url is None:
            return data.get("cdn_url")
        return cdn_url

    return lambda data: cloudflare_worker(cdn_url=get_cdn_url(data), url=url)


def __build_project(out_dir: pl.Path = "data_out"):
    project = get_project()
    out_folder = build_map(project, out_folder=out_dir, start=False)
    set_player_directory(out_folder)


def run(workers: List[Callable], path: pl.Path = "data_out"):
    """
    Runs the workers in the order they are passed. The data from previous
    workers is collected into the single dictionary and passed to the next
    worker.
    """
    global __directory

    if __directory is None:
        __build_project(path)

    pass_data = dict(
        {
            "web_dir": __directory,
        }
    )
    for worker in workers:
        res = worker(pass_data)
        pass_data = {**pass_data, **res} if res is not None else pass_data

    __directory = None
