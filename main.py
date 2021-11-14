# Nginx upstream string generator
import fire
import yaml
import ast


class NginxStreamBlock(object):
  """
  Nginx Stream block for load balanced backend.
  """

  def __init__(self):
    self.__upstream_servers = []
    self.__upstream_nnp = []

    # if file exists, load it
    try:
      with open("conf.yaml", "r") as f:
        conf = yaml.safe_load(f)
        self.__upstream_servers = conf["upstream_servers"]
    except:
      print("Error: conf.yaml file found.\n")

  def upstream(self, upstream_servers: list = []):
    """
    Load upstream servers.
    conf.yaml file will be used if no upstream_servers are provided.
    """
    if type(upstream_servers) == str:
      upstream_servers = ast.literal_eval(upstream_servers)

    if upstream_servers:
      self.__upstream_servers = upstream_servers

    return self

  def nnp(self, upstream_nnp: list):
    """
    Load Names and Ports.
    Upstream name and port (nnp) in the format name:port.
    """
    if self.__check_upstream_servers():
      return

    self.__upstream_nnp = upstream_nnp
    self.__main()

  def __check_upstream_servers(self):
    """
    Check if upstream servers are provided.
    """
    if not self.__upstream_servers:
      print("Error: No upstream servers provided.\n")
      return True

  def __generate_block_comment(self, name: str):
    """
    Generate tile for comment block.
    """
    comment_block = f"    # {name}"
    return comment_block

  def __generate_upstream_list(self, port: str):
    """
    Generate list of upstream servers.
    """
    upstream_list = ""
    for nnp in self.__upstream_servers:
      upstream_list += f"server {nnp}:{port};"
      if not nnp == self.__upstream_servers[-1]:
        upstream_list += "\n\t"
    return upstream_list

  def __generate_upstream_block(self, upstream_nnp: str):
    """
    Generate upstream block.
    """
    upstream_block = f"""
    upstream {upstream_nnp.split(":")[0]} {{
        least_conn;
        {self.__generate_upstream_list(upstream_nnp.split(":")[1])}
    }}
    """
    return upstream_block

  def __generate_server_block(self, upstream_nnp: str):
    """
    Generate server block.
    """
    server_block = f"""
    server {{
        listen {upstream_nnp.split(":")[1]};
        proxy_pass {upstream_nnp.split(":")[0]};
    }}
    """
    return server_block

  def __main(self):
    """
    Main function.
    """
    # if not self.__upstream_servers:
    #   print("No upstream servers provided.")
    #   return

    combined_blocks = []
    for nnp in self.__upstream_nnp:
      comment = self.__generate_block_comment(nnp.split(":")[0])
      upstream_block = self.__generate_upstream_block(nnp).rstrip()
      server_block = self.__generate_server_block(nnp)
      combined_block = comment + upstream_block + server_block
      combined_blocks.append(combined_block)

    for combined_block in combined_blocks:
      print(combined_block)


if __name__ == "__main__":
  fire.Fire(NginxStreamBlock)
