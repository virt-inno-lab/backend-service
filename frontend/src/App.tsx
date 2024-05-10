import React, {useEffect, useState} from "react";
import {Box, Button, Container, Flex, Group, MantineProvider, Textarea, TextInput} from "@mantine/core";
import {isEmail, isNotEmpty, useForm} from "@mantine/form";
import axios, {AxiosError} from "axios";
import {notifications, Notifications} from "@mantine/notifications";

type Cap = "ydb-auditor" | "cloud-auditor" | "cloud-viewer";

const AllCaps: Cap[] = ["ydb-auditor", "cloud-auditor", "cloud-viewer"];

export function App() {
    const form = useForm({
        mode: "controlled",
        initialValues: {
            email: "",
            reason: ""
        },

        validate: {
            email: isEmail("Invalid email"),
            reason: isNotEmpty("Must be filled"),
        },
    });
    const [cap, setCap] = useState<Cap>();

    const refreshCaps = async (silent: boolean) => {
        try {
            const d = await axios.get(`/api/get_caps?email=${form.values.email}`);
            setCap(d.data);
            return true;
        } catch (err) {
            console.log(err);
            if (axios.isAxiosError(err)) {
                const axErr = err as AxiosError;
                if (axErr.response.status == 404) {
                    if (!silent)
                        notifications.show({
                            title: "User not found",
                            message: "Please check email address",
                        });
                }
            }
            if (!silent)
                notifications.show({
                    title: "Internal error",
                    message: err
                });
        }
    };

    const manualRefreshCallback = () => {
        if (form.isValid("email")) {
            refreshCaps(false);
        } else {
            form.setFieldError("email", "Invalid email");
        }
    };

    const requestElevation = (newCap: Cap) => {
        if (!form.validate().hasErrors) {
            axios.post("/api/request_elevation", {
                email: form.values.email,
                reason: form.values.reason,
                cap: newCap
            })
                .then(() => notifications.show({title: "Request sent", message: "You could check logs now"}))
                .catch((err) => notifications.show({title: "Internal error", message: err}));
        }
    };
    useEffect(() => {
        if (form.isValid("email")) {
            refreshCaps(true);
        }
    }, [form.values.email]);

    return <MantineProvider defaultColorScheme="auto">
        <Notifications/>
        <Container>
            <Group justify="center" mb="md">
                <h1>IAM Service</h1>
            </Group>
            <Box maw={480} mx="auto">
                <TextInput
                    withAsterisk
                    label="Email"
                    placeholder="your@email.com"
                    mb="md"
                    key={form.key("email")}
                    {...form.getInputProps("email")}
                />
                <Textarea
                    withAsterisk
                    autosize
                    minRows={2}
                    maxRows={6}
                    label="Reason"
                    placeholder="Describe your reasons for access rights escalation"
                    mb="md"
                    key={form.key("reason")}
                    {...form.getInputProps("reason")}
                />
                <Group justify="flex-end" mb="md">
                    <Button variant="default" mb="md" onClick={manualRefreshCallback}>Manual refresh</Button>
                </Group>
                {cap && AllCaps.filter(e => e !== cap).map(c => <Button>{c}</Button>)}
            </Box>
        </Container>
    </MantineProvider>;
}