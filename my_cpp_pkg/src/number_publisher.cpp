#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class NumberPublisher : public rclcpp::Node
{
public:
    NumberPublisher() : Node("number_publisher")
    {
        publisher_ = this->create_publisher<example_interfaces::msg::String>("number",10);
        timer_ = this -> create_wall_timer(std::chrono::milliseconds(500), std::bind(&NumberPublisher::publishNumber,this));
        RCLCPP_INFO(this -> get_logger(), "Number publisher has been started.");
    }
private:
    void publishNumber(){
        auto msg = example_interfaces::msg::String();
        msg.data = std::string("777");
        publisher_ -> publish(msg);
    }

    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<NumberPublisher>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

