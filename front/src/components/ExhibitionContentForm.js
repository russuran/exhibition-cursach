import React from 'react';
import { Form, Input, Button, Select, message } from 'antd';
import axios from 'axios';

const ExhibitionContentForm = ({ initialValues, onSubmit }) => {
    const [form] = Form.useForm();
    const [exhibits, setExhibits] = React.useState([]);
    const [exhibitions, setExhibitions] = React.useState([]);

    React.useEffect(() => {
        const fetchExhibits = async () => {
            try {
                const response = await axios.get('http://localhost:5000/exhibit_list');
                setExhibits(response.data);
            } catch (error) {
                console.error('Ошибка при получении экспонатов:', error);
                message.error('Не удалось загрузить экспонаты. Пожалуйста, попробуйте позже.');
            }
        };

        const fetchExhibitions = async () => {
            try {
                const response = await axios.get('http://localhost:5000/exhibitions_list');
                console.log(2, response.data);
                setExhibitions(response.data);
            } catch (error) {
                console.error('Ошибка при получении выставок:', error);
                message.error('Не удалось загрузить выставки. Пожалуйста, попробуйте позже.');
            }
        };

        fetchExhibits();
        fetchExhibitions();
    }, []);

    React.useEffect(() => {
        if (initialValues) {
            form.setFieldsValue(initialValues);
        } else {
            form.resetFields();
        }
    }, [initialValues, form]);

    const handleFinish = (values) => {
        onSubmit(values);
    };

    return (
        <Form 
            form={form} 
            onFinish={handleFinish} 
            labelCol={{ span: 10 }} 
            layout="vertical" 
            style={{ maxWidth: 600 }}
        >
            <Form.Item 
                name="exhibit_id" 
                label="Экспонат" 
                rules={[{ required: true, message: 'Пожалуйста, выберите экспонат' }]}
            >
                <Select placeholder="Выберите экспонат">
                    {exhibits.map(exhibit => (
                        <Select.Option key={exhibit.id} value={exhibit.id}>
                            {exhibit.name}
                        </Select.Option>
                    ))}
                </Select>
            </Form.Item>
            <Form.Item 
                name="exhibition_id" 
                label="Выставка" 
                rules={[{ required: true, message: 'Пожалуйста, выберите выставку' }]}
            >
                <Select placeholder="Выберите выставку">
                    {exhibitions.map(exhibition => (
                        <Select.Option key={exhibition.id} value={exhibition.name}>
                            {exhibition.title}
                        </Select.Option>
                    ))}
                </Select>
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Сохранить
                </Button>
            </Form.Item>
        </Form>
    );
};

export default ExhibitionContentForm;
