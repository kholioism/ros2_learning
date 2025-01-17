#include "rclcpp/rclcpp.hpp"

class MyCustomeNode : public rclcpp::Node
{
public:
    MyCustomeNode() : Node("node_name")
    {
    }
private:
};

int main(int argc, char **argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<MyCustomeNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

